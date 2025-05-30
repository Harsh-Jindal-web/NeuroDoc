import streamlit as st
from graphviz import Digraph

def show_flowchart_detailed():

    flow = Digraph()
    flow.attr(rankdir='TB', size='10')

    # Upload and Load
    flow.node("A1", "📤 Upload Document\n(PDF or TXT)", shape="box", style="filled", fillcolor="#e3f2fd")
    flow.node("A2", "📄 Read & Convert to Text", shape="box")

    # Processing
    flow.node("B1", "✂️ Split into Chunks", shape="box", style="filled", fillcolor="#f1f8e9")
    flow.node("B2", "🧠 Generate Embeddings\n(using AzureOpenAI)", shape="box")
    flow.node("B3", "🗃️ Store in Vectorstore (FAISS)", shape="box")

    # User Action
    flow.node("C1", "📌 Choose Task\n(e.g. Extract Entities, Chat)", shape="box", style="filled", fillcolor="#fff3e0")

    # Task Branch
    flow.node("D1", "🧾 Run Prompt-based Extraction\n(Entities, Obligations, etc.)", shape="box")
    flow.node("D2", "🤖 Ask Questions\n(via Conversational Chain)", shape="box")

    # Output
    flow.node("E1", "📊 Show Results\n(accordion/code/text)", shape="box", style="filled", fillcolor="#ede7f6")
    flow.node("E2", "💾 Save to Cache / Export", shape="box")

    # Edges
    flow.edge("A1", "A2")
    flow.edge("A2", "B1")
    flow.edge("B1", "B2")
    flow.edge("B2", "B3")
    flow.edge("B3", "C1")
    flow.edge("C1", "D1")
    flow.edge("C1", "D2")
    flow.edge("D1", "E1")
    flow.edge("D2", "E1")
    flow.edge("E1", "E2")

    st.graphviz_chart(flow)
