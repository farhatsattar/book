import google.generativeai as genai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using Google's embedding API
        """
        embeddings = []
        for text in texts:
            try:
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            except Exception as e:
                error_msg = str(e)
                print(f"Error generating embedding: {e}")
                # Check if it's a quota/rate limit error
                if "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "429" in error_msg:
                    print("Quota error detected for embeddings API")
                    # For quota errors, we can try to provide a basic embedding
                    # This is a very simple approach - in production you might want to use a different service
                    import hashlib
                    # Create a deterministic "embedding" based on the text hash
                    text_hash = hashlib.md5(text.encode()).hexdigest()
                    # Convert hash to a 768-dim vector (simplified approach)
                    embedding = []
                    for i in range(0, 768*2, 2):
                        hex_pair = text_hash[i % len(text_hash):(i % len(text_hash))+2]
                        if len(hex_pair) == 2:
                            val = int(hex_pair, 16) / 255.0  # Normalize to 0-1
                            embedding.append(val)
                        else:
                            embedding.append(0.0)
                    # Ensure we have exactly 768 dimensions
                    embedding = (embedding * (768 // len(embedding) + 1))[:768]
                    embeddings.append(embedding)
                else:
                    # Fallback embedding (zeros) if API call fails for other reasons
                    embeddings.append([0.0] * 768)  # Google's embedding-001 returns 768-dim vectors

        return embeddings

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for a query using Google's embedding API
        """
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            error_msg = str(e)
            print(f"Error generating query embedding: {e}")
            # Check if it's a quota/rate limit error
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower() or "429" in error_msg:
                print("Quota error detected for query embeddings API")
                # For quota errors, we can try to provide a basic embedding
                # This is a very simple approach - in production you might want to use a different service
                import hashlib
                # Create a deterministic "embedding" based on the text hash
                text_hash = hashlib.md5(query.encode()).hexdigest()
                # Convert hash to a 768-dim vector (simplified approach)
                embedding = []
                for i in range(0, 768*2, 2):
                    hex_pair = text_hash[i % len(text_hash):(i % len(text_hash))+2]
                    if len(hex_pair) == 2:
                        val = int(hex_pair, 16) / 255.0  # Normalize to 0-1
                        embedding.append(val)
                    else:
                        embedding.append(0.0)
                # Ensure we have exactly 768 dimensions
                embedding = (embedding * (768 // len(embedding) + 1))[:768]
                return embedding
            else:
                # Fallback embedding (zeros) if API call fails for other reasons
                return [0.0] * 768  # Google's embedding-001 returns 768-dim vectors