import os
import sys
import requests
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

# Add the project root directory to the path so imports work
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from backend.rag.embeddings import EmbeddingGenerator
from backend.qdrant.vector_db import VectorDB

def extract_text_from_webpage(url: str) -> dict:
    """
    Extract text content from a deployed webpage
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

        # Extract title from the page
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "Unknown Title"

        # Extract main heading if available
        main_heading = soup.find(['h1', 'h2'])
        if main_heading:
            title = main_heading.get_text().strip()

        return {
            "content": text,
            "url": url,
            "title": title,
            "source": "deployed-book",
            "metadata": {
                "url": url,
                "domain": "book-5zp6.vercel.app"
            }
        }
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
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

def replace_placeholder_urls():
    """
    Get the actual URLs by replacing placeholder domain with real domain
    """
    base_url = "https://book-5zp6.vercel.app"

    # List of relative paths from the sitemap (without the placeholder domain)
    paths = [
        "/",
        "/docs/",
        "/docs/chapter1/",
        "/docs/chapter2/",
        "/docs/chapter2/applications",
        "/docs/chapter2/challenges",
        "/docs/chapter2/embodied-foundations",
        "/docs/chapter2/humanoid-design",
        "/docs/chapter3/",
        "/docs/chapter3/actuator-technologies",
        "/docs/chapter3/applications",
        "/docs/chapter3/integration",
        "/docs/chapter3/sensor-fundamentals",
        "/docs/chapter4/",
        "/docs/chapter4/applications",
        "/docs/chapter4/control-architecture",
        "/docs/chapter4/integration",
        "/docs/chapter4/ros2-fundamentals",
        "/docs/chapter5/",
        "/docs/chapter5/action-systems",
        "/docs/chapter5/ai-perception",
        "/docs/chapter5/case-studies",
        "/docs/chapter5/challenges-future",
        "/docs/chapter5/integration-architectures",
        "/docs/chapter5/perception-action-loop",
        "/docs/chapter5/sensor-integration",
        "/docs/intro",
        "/docs/tutorial-basics/congratulations",
        "/docs/tutorial-basics/create-a-blog-post",
        "/docs/tutorial-basics/create-a-document",
        "/docs/tutorial-basics/create-a-page",
        "/docs/tutorial-basics/deploy-your-site",
        "/docs/tutorial-basics/markdown-features",
        "/docs/tutorial-extras/manage-docs-versions",
        "/docs/tutorial-extras/translate-your-site"
    ]

    urls = [base_url + path for path in paths]
    return urls

def ingest_from_vercel():
    """
    Ingest content from the deployed Vercel site
    """
    print("Starting content ingestion from deployed Vercel site...")

    # Initialize components
    embedding_gen = EmbeddingGenerator()
    vector_db = VectorDB(collection_name="rag_documents")

    # Get URLs to process
    urls = replace_placeholder_urls()
    print(f"Found {len(urls)} URLs to process")

    all_documents = []

    for url in urls:
        print(f"Processing: {url}")

        try:
            # Extract content from the webpage
            doc = extract_text_from_webpage(url)
            if not doc:
                continue

            # Chunk the content
            content_chunks = chunk_text(doc["content"])

            for i, chunk in enumerate(content_chunks):
                chunk_doc = {
                    "content": chunk,
                    "url": f"{doc['url']}#chunk-{i}",
                    "title": f"{doc['title']} - Chunk {i+1}",
                    "source": "deployed-book",
                    "metadata": {
                        **doc["metadata"],
                        "chunk_id": i,
                        "total_chunks": len(content_chunks)
                    }
                }
                all_documents.append(chunk_doc)

        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

    print(f"Extracted {len(all_documents)} document chunks")

    if not all_documents:
        print("No documents to process")
        return []

    # Extract content for embedding
    contents = [doc["content"] for doc in all_documents]

    # Generate embeddings
    print("Generating embeddings...")
    embeddings = embedding_gen.generate_embeddings(contents)

    # Store in vector database
    print("Storing in vector database...")
    ids = vector_db.store_documents(all_documents, embeddings)

    print(f"Successfully stored {len(ids)} documents in vector database")
    print("Ingestion from deployed site completed!")

    return ids

if __name__ == "__main__":
    ingest_from_vercel()