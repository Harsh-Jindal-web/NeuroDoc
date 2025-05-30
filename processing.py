from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Function to load and split a plain text (.txt) file into smaller chunks
def load_txt_and_split(filepath):
    loader = TextLoader(filepath)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)

# Function to load and split a PDF file into smaller chunks
def load_pdf_and_split(filepath):
    loader = PyPDFLoader(filepath)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)
