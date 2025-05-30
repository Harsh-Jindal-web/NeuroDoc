# 🤖 NeuroDoc: Legal Document AI Assistant

NeuroDoc is an intelligent legal document analysis tool built with Streamlit, LangChain, and Azure OpenAI services. It allows users to upload PDF or TXT legal documents and perform various AI-powered actions such as extracting obligations, rights, responsibilities, license types, risks, compliance details, entity extraction, and interactive Q&A over the document content.

---

## 🚀 Features

- 📄 Upload and preview legal documents (PDF/TXT)
- ✂️ Split and embed content using Azure OpenAI
- 🔍 Extract:
  - Entities
  - Obligations
  - Responsibilities
  - Rights
  - License Types
  - Risks
  - Compliance Clauses
- 💬 Chat with your document (retrieval-augmented QA)
- 📈 View results in tables or expandable views
- 💾 Export results as JSON/CSV
- 📊 Visual agent workflow diagram
  
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

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Harsh-Jindal-web/NeuroDoc.git
cd NeuroDoc
```
### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Azure OpenAI
```bash
You can also add .env support using python-dotenv.
```
### 5. Run the App
```bash
streamlit run app.py
```

Then open your browser to: http://localhost:8501

## 🤔 How to contribute

- Fork this repository;
- Create a branch with your feature: `git checkout -b my-feature`;
- Commit your changes: `git commit -m "feat: my new feature"`;
- Push to your branch: `git push origin my-feature`.

Once your pull request has been merged, you can delete your branch.

## 📜 License

This project is licensed under the [MIT License](LICENSE).
