import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any
import time
from .embeddings import EmbeddingGenerator
from ..qdrant.vector_db import VectorDB

class DocumentIngestor:
    def __init__(self, embedding_generator: EmbeddingGenerator, vector_db: VectorDB):
        self.embedding_generator = embedding_generator
        self.vector_db = vector_db

    def extract_text_from_url(self, url: str) -> Dict[str, Any]:
        """
        Extract text content from a URL
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return {
                "content": text,
                "url": url,
                "title": soup.title.string if soup.title else "",
                "source": "web",
                "metadata": {
                    "domain": urlparse(url).netloc,
                    "timestamp": time.time()
                }
            }
        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into chunks of specified size with overlap
        """
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            # Move start position by chunk_size - overlap
            start = end - overlap

            # If remaining text is less than chunk_size, take it as the last chunk
            if len(text) - start < chunk_size:
                if start < len(text):
                    chunks.append(text[start:])
                break

        return chunks

    def process_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Process a list of URLs and extract documents
        """
        documents = []

        for url in urls:
            print(f"Processing URL: {url}")
            doc = self.extract_text_from_url(url)

            if doc:
                # Chunk the content
                content_chunks = self.chunk_text(doc["content"])

                for i, chunk in enumerate(content_chunks):
                    chunk_doc = {
                        "content": chunk,
                        "url": f"{doc['url']}#chunk-{i}",
                        "title": f"{doc['title']} - Chunk {i+1}",
                        "source": "web",
                        "metadata": {
                            **doc["metadata"],
                            "chunk_id": i,
                            "total_chunks": len(content_chunks)
                        }
                    }
                    documents.append(chunk_doc)

            # Add a small delay to avoid overwhelming servers
            time.sleep(0.5)

        return documents

    def ingest_documents(self, urls: List[str]):
        """
        Ingest documents from URLs into the vector database
        """
        # Extract documents from URLs
        documents = self.process_urls(urls)

        if not documents:
            print("No documents to process")
            return []

        print(f"Extracted {len(documents)} document chunks")

        # Extract content for embedding
        contents = [doc["content"] for doc in documents]

        # Generate embeddings
        print("Generating embeddings...")
        embeddings = self.embedding_generator.generate_embeddings(contents)

        # Store in vector database
        print("Storing in vector database...")
        ids = self.vector_db.store_documents(documents, embeddings)

        print(f"Successfully stored {len(ids)} documents in vector database")
        return ids