from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chatbot import ResumeChatbot
from rag import rebuild_vectorstore


 
# Paths
 

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "uploaded_files"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"


DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


 
# FastAPI
 

app = FastAPI(
    title="CareerCopilot API",
    description="AI-powered resume assistant using RAG and LLMs",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


 
# Frontend
 

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
def home():

    index_file = TEMPLATES_DIR / "index.html"

    return index_file.read_text(
        encoding="utf-8"
    )


 
# Chatbot
 

chatbot = None


 
# Request / Response Models
 

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


 
# Health Check
 

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


 
# Upload CV
 

@app.post("/upload")
async def upload_cv(
    file: UploadFile = File(...)
):

    global chatbot

    allowed_extensions = {
        ".pdf",
        ".docx"
    }

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )


    # Remove previous uploaded files
    for existing_file in DATA_DIR.iterdir():

        if existing_file.is_file():

            existing_file.unlink()


    # Save new CV
    file_path = DATA_DIR / file.filename

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    try:

        # Create a new FAISS vector store
        rebuild_vectorstore()

        # Create chatbot using the new vector store
        chatbot = ResumeChatbot()

    except Exception as error:

        # Remove invalid upload
        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process resume: {str(error)}"
        )


    return {
        "message": "Resume uploaded and processed successfully.",
        "filename": file.filename
    }


 
# Chat

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat_endpoint(
    request: ChatRequest
):

    global chatbot

    if chatbot is None:

        raise HTTPException(
            status_code=400,
            detail="Please upload a resume before asking questions."
        )


    try:

        answer = chatbot.ask(
            request.message
        )

        return ChatResponse(
            response=answer
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(error)}"
        )