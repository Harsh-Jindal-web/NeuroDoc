import streamlit as st
from langchain.schema import SystemMessage, HumanMessage
from streamlit_pdf_viewer import pdf_viewer
import hashlib, fitz
import datetime
import pandas as pd
import io
import json

# Function to generate SHA256 hash of uploaded file's content
def get_file_hash(file_bytes):
    """Generate SHA256 hash of uploaded file content."""
    return hashlib.sha256(file_bytes).hexdigest()

# Sidebar UI to show file info and let user choose an action
def sidebar_ui(uploaded_file):
    with st.sidebar:
        if uploaded_file:
            st.success(f"Uploaded: {uploaded_file.name}")
            
            st.sidebar.markdown("### 📊 File Info")
            file_size_kb = uploaded_file.size / 1024
            st.sidebar.write(f"**Filename:** `{uploaded_file.name}`")
            st.sidebar.write(f"**File size:** {file_size_kb:.2f} KB")
            upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.sidebar.write(f"**Uploaded at:** {upload_time}")
            st.markdown("---")
            st.subheader("🔍 Select Action")

            action = st.radio("Choose what to extract:", [
                "Extract Entities",
                "Extract Obligations",
                "Extract Responsibilities",
                "Extract Rights",
                "Extract License Type",
                "Extract Risks",
                "Extract Compliance",
                "Chat with PDF"
            ])
            return action
        else:
            st.info("📤 Upload a file to continue")
            return None


# Display a PDF document in the main app window
def display_uploaded_file(filepath, file_ext):
    st.markdown("""
    <h3 style='text-align: center;'>📄 Uploaded Document Preview</h3>
""", unsafe_allow_html=True)

    if file_ext == "pdf":
        import fitz
        doc = fitz.open(filepath)
        total_pages = doc.page_count
        doc.close()

        if 'page_num' not in st.session_state:
            st.session_state.page_num = 1

        page_num = st.slider("Select page", 1, total_pages, st.session_state.page_num)
        st.session_state.page_num = page_num

        pdf_viewer(filepath, pages_to_render=[page_num],height=650)
        st.write(f"Page {page_num} of {total_pages}")


# Display results in accordion-style expandable panels
def show_result_area_accordion(title, data_list):
    import streamlit as st
    import json
    st.markdown(f"### {title}")
    for i, item in enumerate(data_list):
        with st.expander(f"Item {i+1}"):
            if isinstance(item, dict) or isinstance(item, list):
                st.json(item)
            else:
                st.write(item)
            if isinstance(item, str):
                if st.button(f"Copy Item {i+1}", key=f"copy_{i}"):
                    st.experimental_set_clipboard(item)
                    st.success("Copied to clipboard!")

# Convert entity extraction result into a table
# def show_entities_table(entities_result):
#     data = []
#     for entity_item in entities_result:
#         if ": " in entity_item:
#             entity, content = entity_item.split(": ", 1)
#             data.append({"Entity": entity.strip("* "), "Content": content})
#     df = pd.DataFrame(data)
#     st.table(df)

# Allow users to export data in JSON, CSV, or TXT format
def export_data(data, filename_base="extracted_data"):
    if isinstance(data, list):
        json_str = json.dumps(data, indent=2)
        st.download_button("Download JSON", json_str, file_name=f"{filename_base}.json")
        try:
            import pandas as pd
            df = pd.DataFrame(data)
            csv_data = df.to_csv(index=False)
            st.download_button("Download CSV", csv_data, file_name=f"{filename_base}.csv")
        except:
            pass
    elif isinstance(data, str):
        st.download_button("Download Text", data, file_name=f"{filename_base}.txt")
