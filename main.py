import os
import json
import streamlit as st
from langchain.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage, HumanMessage

from processing import load_pdf_and_split, load_txt_and_split
from prompts import (
    prompts_list, obligations_prompt, responsibility_prompt, rights_prompt,
    licence_type_prompt, risk_prompt, compliance_prompt
)
from ui_utils import *
from assets.flowchart import show_flowchart_detailed
import time , datetime

# === Azure OpenAI API Configuration ===
os.environ["OPENAI_API_TYPE"] = ""
os.environ["OPENAI_API_VERSION"] = ""
os.environ["OPENAI_API_KEY"] = ""

LLM_DEPLOYMENT_NAME = ""
EMBEDDING_DEPLOYMENT_NAME = ""

# Initialize embeddings client with Azure configuration
embeddings = AzureOpenAIEmbeddings(
    deployment=EMBEDDING_DEPLOYMENT_NAME,
    azure_endpoint="",
    api_key=os.environ["OPENAI_API_KEY"],
)


# Initialize language model client with Azure configuration
llm = AzureChatOpenAI(
    deployment_name=LLM_DEPLOYMENT_NAME,
    azure_endpoint="",
    openai_api_key=os.environ["OPENAI_API_KEY"],
)


# Initialize session state for showing workflow diagram toggle
if "show_workflow" not in st.session_state:
    st.session_state.show_workflow = False


def cache_filepath_entities_obligations(filename):
    """Return path for caching entities and obligations extraction results."""
    folder = "caches"
    os.makedirs(folder, exist_ok=True)
    safe_name = filename.replace(".", "_")
    return os.path.join(folder, f"{safe_name}_entities_obligations.json")

def cache_filepath_other_actions(filename):
    """Return path for caching results of other extraction tasks."""
    folder = "caches"
    os.makedirs(folder, exist_ok=True)
    safe_name = filename.replace(".", "_")
    return os.path.join(folder, f"{safe_name}_other_actions.json")

def get_faiss_cache_dir(file_hash):
    """Return directory path to cache FAISS vectorstore for a specific file hash."""
    folder = "faiss_cache"
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, file_hash)

def load_or_create_vectorstore(chunks, embeddings, file_hash):
    """Load FAISS vectorstore cache if exists; otherwise create and save it."""
    cache_dir = get_faiss_cache_dir(file_hash)
    if os.path.exists(cache_dir):
        return FAISS.load_local(cache_dir, embeddings, allow_dangerous_deserialization=True)
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    vectorstore.save_local(cache_dir)
    return vectorstore

def load_cached_response(filename, action):
    """
    Load cached extracted content for given filename and action.
    Differentiate cache files for entities/obligations vs other actions.
    """
    if action in ["Extract Entities", "Extract Obligations"]:
        path = cache_filepath_entities_obligations(filename)
    else:
        path = cache_filepath_other_actions(filename)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(action.replace("Extract ", "").lower(), None)
    return None

def save_cached_response(filename, action, content):
    """
    Save extracted content for a given filename and action into cache.
    Merge with existing cache data if any.
    """
    if action in ["Extract Entities", "Extract Obligations"]:
        path = cache_filepath_entities_obligations(filename)
    else:
        path = cache_filepath_other_actions(filename)

    data = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    key = action.replace("Extract ", "").lower()
    data[key] = content
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# === Streamlit app layout configuration ===
st.set_page_config(layout="wide")
st.title("🤖 Legal Document AI Assistant")

# Show workflow diagram if toggled on in session state
if st.session_state.show_workflow:
    with st.sidebar:
        if st.button("🔙 Back to Main App"):
            st.session_state.show_workflow = False
            st.rerun()

    # Display the detailed agent workflow flowchart
    show_flowchart_detailed()
    st.title("🧠 Agent Workflow Diagram")
    st.stop()

# Sidebar UI elements
with st.sidebar:
    if st.button("🧩 Agent Workflow"):
        st.session_state.show_workflow = True
        st.rerun()

    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], key="unique_file_upload")
    action = sidebar_ui(uploaded_file)


# Create two columns: one for PDF preview, one for output/results
col_pdf, col_output = st.columns([4, 3])

# When a file is uploaded, proceed to process it
if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    temp_path = f"temp.{file_ext}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    # if file_ext == "pdf":
    #     doc = fitz.open(temp_path)
    #     st.sidebar.write(f"**Pages:** {doc.page_count}")
    #     doc.close()

    # Generate a hash of file content to use as a cache key
    file_bytes = uploaded_file.getbuffer()
    file_hash = get_file_hash(file_bytes)

    # Load and split document into chunks depending on file type
    chunks = load_pdf_and_split(temp_path) if file_ext == "pdf" else load_txt_and_split(temp_path)
    full_text = " ".join(chunk.page_content for chunk in chunks[:5])

    # Load FAISS vectorstore from cache or create if not exists
    vectorstore = load_or_create_vectorstore(chunks, embeddings, file_hash)

    # Initialize memory for conversational chat history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Build conversational retrieval chain for Q&A over the document
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
        memory=memory,
        return_source_documents=True,
        output_key="answer",
    )

    # Show PDF preview on left column
    with col_pdf:
        # show_flowchart()
        display_uploaded_file(temp_path, file_ext)


    # Show extraction/chat results on right column
    with col_output:
        if action:
            # Try to load cached results for the selected action
            cache_data = load_cached_response(file_hash, action)
            if cache_data:
                st.success(f"Loaded cached result for **{action}**")
                if isinstance(cache_data, list):
                    show_result_area_accordion(f"📝 {action}", cache_data)
                else:
                    st.code(cache_data)
            else:
                # If no cache, perform the selected extraction or chat task
                if action == "Extract Entities":
                    with st.spinner("Extracting entities, please wait..."):
                        entities_result = []
                        for item in prompts_list:
                            messages = [
                                SystemMessage(content="You are a legal assistant."),
                                HumanMessage(content=f"{item['Prompt']}\n\nText:\n{full_text}")
                            ]
                            response = llm(messages)
                            entities_result.append(f"**{item['Entity']}**: {response.content}")
                            time.sleep(0.2) 
                        show_result_area_accordion(f"📝 {action}", entities_result)
                        # show_entities_table(entities_result)
                        export_data(entities_result, "entities")

                        save_cached_response(file_hash, action, entities_result)

                elif action == "Extract Obligations":
                    with st.spinner("Extracting Obligations, please wait..."):
                        messages = [
                            SystemMessage(content="You are a legal assistant."),
                            HumanMessage(content=obligations_prompt.format(text=full_text)),
                        ]
                        result = llm(messages)
                        try:
                            parsed = json.loads(result.content)
                        except:
                            parsed = [result.content]
                        time.sleep(0.2) 
                        show_result_area_accordion(f"📝 {action}", parsed)
                        save_cached_response(file_hash, action, parsed)

                elif action == "Chat with PDF":
                    with st.spinner("Extracting entities, please wait..."):
                        st.subheader("💬 Ask about the document")
                        query = st.text_input("Ask a question:")
                        if query:
                            inputs = {
                                "question": query,
                                "chat_history": memory.buffer_as_messages
                            }
                            qa_chain.memory = None
                            full_result = qa_chain.invoke(inputs)
                            memory.save_context({"question": query}, {"answer": full_result["answer"]})
                            qa_chain.memory = memory

                            st.write("### 🤖 Answer")
                            st.write(full_result["answer"])

                            st.markdown("### 📚 Sources")
                            for i, doc in enumerate(full_result["source_documents"]):
                                with st.expander(f"Chunk {i + 1}"):
                                    st.write(doc.page_content)

                else:
                    # Map other extraction actions to their respective prompt templates
                    prompt_map = {
                        "Extract Responsibilities": responsibility_prompt,
                        "Extract Rights": rights_prompt,
                        "Extract License Type": licence_type_prompt,
                        "Extract Risks": risk_prompt,
                        "Extract Compliance": compliance_prompt,
                    }
                    if action in prompt_map:
                        with st.spinner(f"{action}, please wait..."):
                            messages = [
                                SystemMessage(content="You are a legal assistant."),
                                HumanMessage(content=prompt_map[action] + "\n" + full_text),
                            ]
                            result = llm(messages)
                            st.code(result.content)
                            time.sleep(0.2)
                            save_cached_response(file_hash, action, result.content)