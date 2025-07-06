import os
import fitz  # PyMuPDF
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
DEFAULT_INDEX_PATH = "app/faiss_index"
DEFAULT_MODEL = "models/embedding-001"
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 200


def load_pdf_bytes(pdf_path: str) -> list[Document]:
    """Load a PDF and extract text page-wise as LangChain Documents."""
    with open(pdf_path, "rb") as f:
        content = f.read()

    pdf_doc = fitz.open(stream=content, filetype="pdf")
    docs = []

    for i in range(pdf_doc.page_count):
        page = pdf_doc[i]
        text = page.get_text()
        if text.strip():
            docs.append(Document(
                page_content=text,
                metadata={"source": os.path.basename(pdf_path), "page": i + 1}
            ))

    pdf_doc.close()
    return docs


def process_folder(
    folder_path: str,
    index_path: str = DEFAULT_INDEX_PATH,
) -> FAISS:
    """Process PDFs in folder, chunk, embed, build, and save FAISS vectorstore."""
    # Get API key from environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it with your Google API key.")
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model=DEFAULT_MODEL,
        google_api_key=api_key
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=DEFAULT_CHUNK_SIZE, chunk_overlap=DEFAULT_CHUNK_OVERLAP)

    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            docs = load_pdf_bytes(full_path)
            all_docs.extend(docs)

    if not all_docs:
        raise ValueError(f"No PDF files found in '{folder_path}' or all PDFs are empty.")

    chunks = splitter.split_documents(all_docs)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    vectorstore.save_local(index_path)

    print(f"Vectorstore successfully saved to '{index_path}/'.")
    print(f"Use load_vectorstore() to reload the vectorstore.")
    return vectorstore


if __name__ == "__main__":
    vectorstore = process_folder(folder_path="data")