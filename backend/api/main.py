from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import sys
import logging

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.rag.embeddings import EmbeddingGenerator
from backend.qdrant.vector_db import VectorDB
from backend.rag.document_ingestion import DocumentIngestor
from backend.openai_agent.retrieval_agent import RetrievalAgent

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based chatbot with document retrieval capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global components
vector_db = VectorDB(collection_name="rag_documents")
retrieval_agent = RetrievalAgent(vector_db)

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class ChatRequest(BaseModel):
    query: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    top_k: Optional[int] = 5

class DocumentIngestionRequest(BaseModel):
    urls: List[str]

class DocumentResponse(BaseModel):
    response: str
    context_docs: List[Dict[str, Any]]
    query: str

@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API is running!"}

@app.post("/ingest", summary="Ingest documents from URLs")
def ingest_documents(request: DocumentIngestionRequest):
    """
    Ingest documents from provided URLs into the vector database
    """
    try:
        embedding_gen = EmbeddingGenerator()
        ingestor = DocumentIngestor(embedding_gen, vector_db)

        document_ids = ingestor.ingest_documents(request.urls)

        return {
            "message": f"Successfully ingested {len(document_ids)} document chunks",
            "document_ids": document_ids
        }
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error ingesting documents: {str(e)}")

@app.post("/query", response_model=DocumentResponse, summary="Query the RAG system")
def query_documents(request: QueryRequest):
    """
    Query the RAG system to get a response based on retrieved documents
    """
    try:
        result = retrieval_agent.query(request.query, request.top_k)
        return result
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/chat", response_model=DocumentResponse, summary="Chat with conversation history")
def chat(request: ChatRequest):
    """
    Chat with the system, maintaining conversation history
    """
    try:
        result = retrieval_agent.chat_with_history(
            request.query,
            request.conversation_history,
            request.top_k
        )
        return result
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/search", summary="Search documents directly")
def search_documents(query: str = Query(..., min_length=1), top_k: int = Query(5, ge=1, le=20)):
    """
    Direct search of documents in the vector database
    """
    try:
        embedding_gen = EmbeddingGenerator()
        query_embedding = embedding_gen.generate_query_embedding(query)
        results = vector_db.search_documents(query_embedding, limit=top_k)

        return {
            "query": query,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

@app.get("/health", summary="Health check endpoint")
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"status": "healthy", "message": "RAG Chatbot API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)