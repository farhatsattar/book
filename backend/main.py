import os
import sys
from dotenv import load_dotenv
from .qdrant.vector_db import VectorDB
from .openai_agent.retrieval_agent import RetrievalAgent

# Load environment variables
load_dotenv()

def initialize_rag_system(collection_name: str = "rag_documents"):
    """
    Initialize the complete RAG system
    """
    print("Initializing RAG system...")

    # Initialize components
    vector_db = VectorDB(collection_name=collection_name)
    retrieval_agent = RetrievalAgent(vector_db)

    print("RAG system initialized successfully!")

    return vector_db, retrieval_agent

def main():
    """
    Main function to demonstrate the RAG system
    """
    # Initialize the system
    vector_db, retrieval_agent = initialize_rag_system()

    print("\nRAG Chatbot System is ready!")
    print("You can now:")
    print("1. Run the FastAPI server: python -m backend.api.main")
    print("2. Access the API at http://localhost:8000")
    print("3. Use the frontend interface")
    print("4. Or test the system directly using the Python classes")

    # Example usage
    print("\nExample usage:")
    print(">>> from backend.main import initialize_rag_system")
    print(">>> vector_db, retrieval_agent = initialize_rag_system()")
    print(">>> result = retrieval_agent.query('Your question here')")
    print(">>> print(result['response'])")

if __name__ == "__main__":
    main()