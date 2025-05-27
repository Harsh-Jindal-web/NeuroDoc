# Legal Document AI Assistant

This project is a **legal document AI assistant** built with Streamlit, LangChain, and Azure OpenAI services. It allows users to upload PDF or TXT legal documents and perform various AI-powered actions such as extracting obligations, rights, responsibilities, license types, risks, compliance details, entity extraction, and interactive Q&A over the document content.

---

## Features

- **Upload legal documents** in PDF or TXT format.
- **Preview uploaded documents** page by page with easy navigation.
- **Multiple action modes** powered by Azure OpenAI LLM:
  - Extract Entities
  - Extract Obligations
  - Extract Responsibilities
  - Extract Rights
  - Extract License Type
  - Extract Risks
  - Extract Compliance
  - Chat with PDF (conversational Q&A)
- **Vector-based document retrieval** for efficient similarity search in large documents.
- **Caching** of AI responses for faster repeat queries without repeated calls to the API.
- **Session state management** to preserve uploaded files, document splits, embeddings, and chat history without reprocessing on page reloads.
- **Clean, interactive UI** with sidebar controls and multi-column layout for previews, flowcharts, and results.

---

## How It Works

1. User uploads a PDF or TXT legal document.
2. The app shows a **document preview** with page navigation controls (pagination can be extended).
3. User selects an **action** from the sidebar to analyze or query the document.
4. On first action, the document is split into chunks and embedded with Azure OpenAI embeddings.
5. A vector store is created for efficient semantic search.
6. The selected prompt is sent to the Azure Chat LLM to extract or answer based on the document.
7. Results are cached locally to avoid repeat API calls on subsequent requests.
8. Users can interactively ask questions about the document in “Chat with PDF” mode.

---

## Tech Stack

- **Streamlit** — Web app framework for Python, great for rapid prototyping.
- **LangChain** — Framework for building LLM-powered applications with memory and retrieval chains.
- **Azure OpenAI** — GPT and embedding models hosted on Azure.
- **Chroma** — Vector database for storing document embeddings.
- **PyMuPDF (fitz)** — For extracting PDF text.
- **Local caching** — JSON files to store results for faster access.

---
