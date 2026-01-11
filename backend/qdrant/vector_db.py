from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any
import uuid
import os

class VectorDB:
    def __init__(self, collection_name: str = "rag_documents_1536"):
        import os
        from dotenv import load_dotenv
        load_dotenv()

        # Use cloud Qdrant instance for production, local for development
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if qdrant_url and qdrant_api_key:
            # Use cloud instance for production (Render deployment)
            self.client = QdrantClient(
                url=qdrant_url,
                api_key=qdrant_api_key,
                https=True
            )
        else:
            # Fallback to local instance for development
            self.client = QdrantClient(path="./qdrant_data")

        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        try:
            self.client.get_collection(self.collection_name)
            print(f"Collection {self.collection_name} already exists.")
        except:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # OpenAI text-embedding-3-small dimension
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection {self.collection_name} created.")

    def store_documents(self, documents: List[Dict[str, Any]], embeddings, batch_size: int = 50):
        all_ids = []

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

    # 🔹 ADD THIS METHOD
    def search_documents(self, query_embedding: list, limit: int = 5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        return [
            {
                "content": r.payload.get("content"),
                "url": r.payload.get("url"),
                "title": r.payload.get("title"),
                "score": r.score
            }
            for r in results
        ]
