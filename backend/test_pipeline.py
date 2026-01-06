import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.rag.embeddings import EmbeddingGenerator
from backend.qdrant.vector_db import VectorDB
from backend.rag.document_ingestion import DocumentIngestor

def test_ingestion_pipeline():
    """
    Test the complete ingestion pipeline (Spec 1 and 2)
    """
    print("Testing RAG ingestion pipeline...")

    # Initialize components
    embedding_gen = EmbeddingGenerator()
    vector_db = VectorDB(collection_name="test_rag_documents")
    ingestor = DocumentIngestor(embedding_gen, vector_db)

    # Test URLs (you can replace these with actual URLs for your project)
    test_urls = [
        "https://docs.ros.org/en/humble/",
        "https://python.langchain.com/docs/get_started/introduction",
        "https://platform.openai.com/docs/introduction"
    ]

    print("Starting document ingestion...")
    document_ids = ingestor.ingest_documents(test_urls)

    print(f"Ingested {len(document_ids)} documents")

    # Test retrieval (Spec 2)
    print("\nTesting retrieval functionality...")
    query = "What are the basics of robotics?"
    query_embedding = embedding_gen.generate_query_embedding(query)

    results = vector_db.search_documents(query_embedding, limit=3)

    print(f"Retrieved {len(results)} documents for query: '{query}'")
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        print(f"  Content preview: {result['content'][:100]}...")
        print(f"  URL: {result['url']}")
        print(f"  Score: {result['score']}")
        print()

    # Clean up test collection
    vector_db.delete_collection()
    print("Test completed successfully!")

if __name__ == "__main__":
    load_dotenv()  # Load environment variables

    # Check if required environment variables are set
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is not set!")
        print("Please set your Gemini API key in a .env file")
        sys.exit(1)

    test_ingestion_pipeline()