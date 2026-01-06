import os
import sys

# Add the project root directory to the path so imports work
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from backend.qdrant.vector_db import VectorDB

def reset_vector_db():
    """
    Reset the vector database by deleting and recreating the collection with correct dimensions
    """
    print("Resetting vector database collection...")

    # Create a new VectorDB instance
    vector_db = VectorDB(collection_name="rag_documents")

    # Delete the existing collection
    try:
        vector_db.client.delete_collection("rag_documents")
        print("Deleted existing collection 'rag_documents'")
    except Exception as e:
        print(f"Collection might not exist yet, continuing... Error: {e}")

    # Recreate the collection (this will use the correct 768 dimensions)
    vector_db._create_collection()
    print("Recreated collection 'rag_documents' with correct dimensions (768)")

    # Verify the collection was created with correct settings
    try:
        collection_info = vector_db.client.get_collection("rag_documents")
        print(f"Collection info: {collection_info.config.params}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print(f"Distance: {collection_info.config.params.vectors.distance}")
    except Exception as e:
        print(f"Error getting collection info: {e}")

    print("Vector database reset completed!")

if __name__ == "__main__":
    reset_vector_db()