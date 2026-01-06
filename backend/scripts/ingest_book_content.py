import os
import sys
import glob
from pathlib import Path
import markdown
from bs4 import BeautifulSoup

# Add the backend directory to the path so imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embeddings import EmbeddingGenerator
from qdrant.vector_db import VectorDB

def extract_text_from_markdown(file_path: str) -> dict:
    """
    Extract text content from a markdown file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert markdown to HTML, then extract text
    html = markdown.markdown(content)
    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text content
    text = soup.get_text()

    # Clean up text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)

    # Extract title from the first heading
    title = ""
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            title = line.strip()[2:]  # Remove '# ' prefix
            break

    if not title:
        title = Path(file_path).stem

    return {
        "content": text,
        "url": f"file://{file_path}",
        "title": title,
        "source": "book",
        "metadata": {
            "file_path": file_path,
            "file_name": Path(file_path).name,
            "chapter": extract_chapter_info(file_path)
        }
    }

def extract_chapter_info(file_path: str) -> str:
    """
    Extract chapter information from the file path
    """
    path_parts = Path(file_path).parts
    for part in path_parts:
        if part.startswith('chapter'):
            return part
    return 'unknown'

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

def ingest_book_content():
    """
    Ingest all book content from the docs directory into Qdrant
    """
    print("Starting book content ingestion...")

    # Initialize components
    embedding_gen = EmbeddingGenerator()
    vector_db = VectorDB(collection_name="rag_documents")

    # Find all markdown files in the docs directory (relative to the project root)
    project_root = Path(__file__).parent.parent.parent  # Go up 3 levels to project root
    docs_path = project_root / "ai-native-book" / "docs"
    markdown_files = list(docs_path.rglob("*.md"))

    print(f"Found {len(markdown_files)} markdown files to process")

    all_documents = []

    for file_path in markdown_files:
        print(f"Processing: {file_path}")

        try:
            # Extract content from markdown file
            doc = extract_text_from_markdown(str(file_path))

            # Chunk the content
            content_chunks = chunk_text(doc["content"])

            for i, chunk in enumerate(content_chunks):
                chunk_doc = {
                    "content": chunk,
                    "url": f"{doc['url']}#chunk-{i}",
                    "title": f"{doc['title']} - Chunk {i+1}",
                    "source": "book",
                    "metadata": {
                        **doc["metadata"],
                        "chunk_id": i,
                        "total_chunks": len(content_chunks)
                    }
                }
                all_documents.append(chunk_doc)

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

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
    print("Ingestion completed!")

    return ids

if __name__ == "__main__":
    ingest_book_content()