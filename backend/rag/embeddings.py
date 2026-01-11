
# backend/openai_agent/embeddings.py
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# Load env variables
load_dotenv()

# # Check if API key exists
# if "OPENAI_API_KEY" not in os.environ:
#     raise RuntimeError("❌ OPENAI_API_KEY not found in environment variables")

# OpenAI client (NEW SDK) - set API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class EmbeddingGenerator:
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name
        self.embedding_dim = 1536  # fixed size for embedding-3-small

    # ------------------------------------
    # Generate embeddings for documents
    # ------------------------------------
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[List[float]] = []

        for text in texts:
            try:
                response = client.embeddings.create(
                    model=self.model_name,
                    input=text,
                )
                embeddings.append(response.data[0].embedding)

            except Exception as e:
                print(f"❌ Error generating embedding: {e}")
                embeddings.append([0.0] * self.embedding_dim)

        return embeddings

    # ------------------------------------
    # Generate embedding for query
    # ------------------------------------
    def generate_query_embedding(self, query: str) -> List[float]:
        try:
            response = client.embeddings.create(
                model=self.model_name,
                input=query,
            )
            return response.data[0].embedding

        except Exception as e:
            print(f"❌ Error generating query embedding: {e}")
            return [0.0] * self.embedding_dim
