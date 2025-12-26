from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class VectorDB:
    def __init__(self, collection_name: str = "rag_documents"):
        # Initialize Qdrant client (using local instance by default)
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=qdrant_url)
        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        """
        Create a collection in Qdrant if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embeddings are 1024-dimensional
                    distance=models.Distance.COSINE
                )
            )

    def store_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Store documents and their embeddings in Qdrant
        """
        points = []
        for doc, embedding in zip(documents, embeddings):
            point_id = str(uuid.uuid4())
            points.append(
                models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "content": doc.get("content", ""),
                        "url": doc.get("url", ""),
                        "title": doc.get("title", ""),
                        "source": doc.get("source", ""),
                        "metadata": doc.get("metadata", {})
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        return [point.id for point in points]

    def search_documents(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for documents similar to the query embedding
        """
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        results = []
        for result in search_results:
            results.append({
                "id": result.id,
                "content": result.payload.get("content", ""),
                "url": result.payload.get("url", ""),
                "title": result.payload.get("title", ""),
                "source": result.payload.get("source", ""),
                "metadata": result.payload.get("metadata", {}),
                "score": result.score
            })

        return results

    def delete_collection(self):
        """
        Delete the collection (useful for testing)
        """
        try:
            self.client.delete_collection(self.collection_name)
        except:
            pass  # Collection might not exist