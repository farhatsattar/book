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
        # Initialize Qdrant client
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        try:
            if qdrant_api_key:
                self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            else:
                # Use local instance without API key
                self.client = QdrantClient(url=qdrant_url)
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}")
            print("Attempting to use local in-memory storage as fallback...")
            # Fallback to in-memory storage for testing purposes
            from qdrant_client.http.exceptions import UnexpectedResponse
            from qdrant_client.local.qdrant_local import QdrantLocal
            self.client = QdrantLocal(location=":memory:")
        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        """
        Create a collection in Qdrant if it doesn't exist
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists.")
        except:
            # Create collection if it doesn't exist
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=768,  # Google embeddings are 768-dimensional
                        distance=models.Distance.COSINE
                    )
                )
                print(f"Collection {self.collection_name} created successfully.")
            except Exception as e:
                # If collection already exists, ignore the error
                if "already exists" in str(e):
                    print(f"Collection {self.collection_name} already exists.")
                else:
                    raise e

    def store_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]], batch_size: int = 50):
        """
        Store documents and their embeddings in Qdrant with batching to handle large datasets
        """
        all_ids = []

        # Process documents in batches to avoid timeout issues
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]

            points = []
            for doc, embedding in zip(batch_docs, batch_embeddings):
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

            batch_ids = [point.id for point in points]
            all_ids.extend(batch_ids)

            print(f"Stored batch {i//batch_size + 1}: {len(batch_ids)} documents")

        return all_ids

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