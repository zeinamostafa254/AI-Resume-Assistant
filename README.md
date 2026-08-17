# AI Resume Assistant

An AI-powered resume assistant that allows users to interact with their CV through natural language.

Instead of manually searching through a resume, users can ask questions such as:

* "What are my strongest technical skills?"
* "What machine learning projects have I worked on?"
* "What programming languages do I know?"
* "Do I have experience with NLP?"
* "Summarize my experience."
* "What skills should I improve for an AI internship?"

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the uploaded resume before generating an answer with an LLM.

---

## Features

*  **Resume-based Question Answering**

  * Ask natural-language questions about your CV.

*  **Semantic Search**

  * Finds relevant resume information using vector embeddings rather than simple keyword matching.

*  **Retrieval-Augmented Generation**

  * Retrieves relevant resume chunks and provides them as context to the LLM.

*  **Conversation Memory**

  * Maintains context across multiple messages in a conversation.

*  **Prompt Engineering**

  * Uses structured prompts to produce accurate and relevant responses.

*  **FastAPI Backend**

  * Provides API endpoints for interacting with the AI assistant.

*  **Vector Database**

  * Uses FAISS for efficient similarity search over resume embeddings.

*  **Modular Architecture**

  * Separates RAG, prompts, memory, chatbot logic, utilities, and API logic into different modules.

---

## System Architecture

```text
                    ┌──────────────────────┐
                    │      User / UI       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │      Backend         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Chatbot         │
                    │       Logic          │
                    └───────┬───────┬──────┘
                            │       │
                  ┌─────────┘       └─────────┐
                  ▼                           ▼
        ┌──────────────────┐       ┌──────────────────┐
        │ Conversation     │       │      RAG         │
        │ Memory           │       │    Pipeline      │
        └──────────────────┘       └────────┬─────────┘
                                            │
                                            ▼
                                  ┌──────────────────┐
                                  │ Embeddings +     │
                                  │ FAISS Retrieval  │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │ Resume Context   │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │       LLM        │
                                  └────────┬─────────┘
                                           │
                                           ▼
                                  ┌──────────────────┐
                                  │ Generated Answer │
                                  └──────────────────┘
```

---

## How RAG Works

Resume Assistant follows a Retrieval-Augmented Generation pipeline.

### 1. Resume Loading

The user's CV is loaded from a PDF document.

### 2. Text Extraction

The textual content is extracted from the resume.

### 3. Text Chunking

The resume is divided into smaller chunks so that relevant sections can be retrieved efficiently.

### 4. Embeddings

Each chunk is converted into a numerical vector representation using an embedding model.

### 5. Vector Storage

The embeddings are stored in a **FAISS vector index**.

### 6. Retrieval

When the user asks a question, the question is converted into an embedding and compared against the stored resume embeddings.

The most relevant chunks are retrieved.

### 7. Generation

The retrieved information is provided to the LLM as context.

The LLM then generates an answer based on the retrieved resume information.

```text
User Question
      │
      ▼
Question Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Relevant Resume Chunks
      │
      ▼
Prompt + Context
      │
      ▼
LLM
      │
      ▼
Final Answer
```

---

## Project Structure

```text
CareerCopilot/
│
├── main.py
├── chatbot.py
├── rag.py
├── prompts.py
├── memory.py
├── utils.py
│
├── data/
│   └── uploaded_cv.pdf
│
├── vectorstore/
│   └── ...
│
├── static/
│   ├── style.css
│   └── ...
│
├── templates/
│   └── index.html
│
├── .env
├── .gitignore
└── README.md
```

---

## Technologies

### Programming Language

* Python

### AI / LLM

* Large Language Models
* Prompt Engineering
* LangChain

### RAG

* Retrieval-Augmented Generation
* Text Chunking
* Embeddings
* Semantic Search
* FAISS

### Backend

* FastAPI
* REST API

### Other

* Python-dotenv
* HTML
* CSS

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>

cd CareerCopilot
```

### 2. Create a virtual environment

Using `uv`:

```bash
uv venv
```

Activate the environment on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
uv pip install -r requirements.txt
```

Or, if using a `pyproject.toml`:

```bash
uv sync
```

## Running the Application

Start the FastAPI server with:

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides automatic API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## Example API Request

```http
POST /chat
```

Example request:

```json
{
    "message": "What machine learning projects are included in my resume?",
    "session_id": "user123"
}
```

Example response:

```json
{
    "response": "Your resume includes several machine learning projects...",
    "session_id": "user123"
}
```

---

## Example Questions

CareerCopilot can answer questions such as:

```text
What are my strongest technical skills?

What programming languages do I know?

Tell me about my machine learning experience.

Which projects demonstrate my NLP skills?

Summarize my education.

What frameworks have I worked with?

Do I have experience with deployment?

What technologies should I highlight when applying for an AI internship?
```

