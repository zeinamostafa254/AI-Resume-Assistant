# load documents (pdf and docx)
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "uploaded_files"
VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "faiss_index"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_documents():
    """
    Load all PDF and DOCX files from the upload directory.
    """

    documents = []

    for file_path in DATA_DIR.iterdir():

        if file_path.suffix.lower() == ".pdf":

            loader = PyPDFLoader(str(file_path))
            documents.extend(loader.load())

        elif file_path.suffix.lower() == ".docx":

            loader = Docx2txtLoader(str(file_path))
            documents.extend(loader.load())

    return documents

# splitting documents into chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents):
    """
    Split documents into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return splitter.split_documents(documents)

# embedding model from HuggingFace
#from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings():
    """
    Initialize the Hugging Face embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

# creating vectorstore using FAISS
from langchain_community.vectorstores import FAISS

def create_vectorstore():
    """
    Create and save a FAISS index.
    """

    documents = load_documents()

    if not documents:
        raise ValueError(
            "No PDF or DOCX files were found."
        )

    chunks = split_documents(documents)

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings,
    )
    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    vectorstore.save_local(
        str(VECTORSTORE_DIR)
    )

    return vectorstore

# loading vectorstore from FAISS index
def load_vectorstore():
    """
    Load an existing FAISS index.
    """

    embeddings = get_embeddings()

    return FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

# retrieving relevant documents from vectorstore
def get_retriever(k=5):
    """
    Return a retriever object.
    """

    vectorstore = load_vectorstore()

    return vectorstore.as_retriever(
        search_kwargs={
            "k": k
        }
    )


def rebuild_vectorstore():
    """
    Delete and recreate the vector store.
    """

    if VECTORSTORE_DIR.exists():

        shutil.rmtree(
            VECTORSTORE_DIR
        )

    return create_vectorstore()