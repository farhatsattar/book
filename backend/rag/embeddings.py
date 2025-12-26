import cohere
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Cohere
        """
        response = self.co.embed(
            texts=texts,
            model="embed-english-v3.0",  # Using Cohere's latest embedding model
            input_type="search_document"
        )
        return response.embeddings

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query using Cohere
        """
        response = self.co.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        )
        return response.embeddings[0]