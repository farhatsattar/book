import os
import sys
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Project root path (for relative imports)
# ------------------------------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# ------------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Imports after path fix
# ------------------------------------------------------------------
from backend.rag.embeddings import EmbeddingGenerator
from backend.qdrant.vector_db import VectorDB
from backend.openai_agent.retrieval_agent import RetrievalAgent
from backend.db.chat_history import ChatHistoryDB
from backend.rag.document_ingestion import DocumentIngestor

# ------------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------------
app = FastAPI(
    title="RAG Chatbot API",
    description="RAG-based chatbot with OpenAI embeddings and Qdrant",
    version="1.0.0",
)

# ------------------------------------------------------------------
# CORS for local frontend dev
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://book-5zp6.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Startup event: initialize vector DB, agent, chat history
# ------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("🚀 Initializing RAG system...")

        vector_db = VectorDB(collection_name="rag_documents_1536")  # 1536-dim for OpenAI
        retrieval_agent = RetrievalAgent(vector_db)

        app.state.vector_db = vector_db
        app.state.retrieval_agent = retrieval_agent

        chat_history_db = ChatHistoryDB()
        await chat_history_db.initialize_db()
        app.state.chat_history_db = chat_history_db

        logger.info("✅ RAG system initialized successfully")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        app.state.vector_db = None
        app.state.retrieval_agent = None
        app.state.chat_history_db = None

# ------------------------------------------------------------------
# Request / Response Models
# ------------------------------------------------------------------
class QueryRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None
    top_k: Optional[int] = 5

class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    conversation_history: Optional[List[Dict[str, str]]] = []
    session_id: Optional[str] = None
    top_k: Optional[int] = 5

class DocumentIngestionRequest(BaseModel):
    urls: List[str]

class DocumentResponse(BaseModel):
    response: str
    context_docs: List[Dict[str, Any]]
    query: str
    confidence: Optional[float] = 0.0
    sources: Optional[List[Dict[str, Any]]] = []
    selected_text: Optional[str] = None
    session_id: Optional[str] = None

# ------------------------------------------------------------------
# Health & root
# ------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "RAG Chatbot API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# ------------------------------------------------------------------
# Ingest documents
# ------------------------------------------------------------------
@app.post("/ingest")
def ingest_documents(req: DocumentIngestionRequest, request: Request):
    vector_db = request.app.state.vector_db
    if vector_db is None:
        raise HTTPException(status_code=503, detail="Vector DB not available")

    try:
        embedding_gen = EmbeddingGenerator()
        ingestor = DocumentIngestor(embedding_gen, vector_db)
        document_ids = ingestor.ingest_documents(req.urls)
        return {
            "message": f"Successfully ingested {len(document_ids)} document chunks",
            "document_ids": document_ids,
        }
    except Exception as e:
        logger.error(f"Ingest error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------------
# Chat endpoint
# ------------------------------------------------------------------
@app.post("/chat", response_model=DocumentResponse)
async def chat(request_data: ChatRequest, request: Request):
    agent = request.app.state.retrieval_agent
    if agent is None:
        raise HTTPException(status_code=503, detail="RAG system not available")

    print("🔥 /chat HIT")
    print("🔥 USER QUERY:", request_data.query)

    result = await agent.chat(
        query=request_data.query,
        top_k=request_data.top_k or 5,
        selected_text=request_data.selected_text,
        session_id=request_data.session_id,
    )

    print("🔥 BOT RESPONSE:", result.get("response"))
    return result

# ------------------------------------------------------------------
# Direct vector search (debug)
# ------------------------------------------------------------------
@app.get("/search")
def search_documents(
    query: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    request: Request = None,
):
    vector_db = request.app.state.vector_db
    if vector_db is None:
        raise HTTPException(status_code=503, detail="Vector DB not available")

    try:
        embedding_gen = EmbeddingGenerator()
        query_embedding = embedding_gen.generate_query_embedding(query)
        results = vector_db.search_documents(query_embedding, limit=top_k)
        return {"query": query, "results": results}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------------------------------------------------
# Run locally
# ------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
