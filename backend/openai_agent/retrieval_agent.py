# backend/openai_agent/retrieval_agent.py
from typing import List, Dict, Optional, Any
from backend.rag.embeddings import EmbeddingGenerator
from backend.qdrant.vector_db import VectorDB
import openai
import logging

logger = logging.getLogger(__name__)

class RetrievalAgent:
    def __init__(self, vector_db: VectorDB, gpt_model: str = "gpt-3.5-turbo"):
        self.vector_db = vector_db
        self.embedding_generator = EmbeddingGenerator()
        self.gpt_model = gpt_model

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
        selected_text: Optional[str] = None
    ) -> List[Dict[str, Any]]:

        query_embedding = self.embedding_generator.generate_query_embedding(query)
        results = self.vector_db.search_documents(query_embedding, limit=top_k)

        if selected_text:
            selected_embedding = self.embedding_generator.generate_query_embedding(selected_text)
            selected_results = self.vector_db.search_documents(selected_embedding, limit=top_k)

            # Combine + deduplicate
            seen_ids = set()
            combined = []
            for r in selected_results + results:
                if r.get("title") not in seen_ids:
                    combined.append(r)
                    seen_ids.add(r.get("title"))
            return combined[:top_k]

        return results

    def generate_response(
        self,
        query: str,
        context_docs: List[Dict[str, Any]],
        selected_text: Optional[str] = None
    ) -> str:
        context_text = ""
        for i, doc in enumerate(context_docs):
            context_text += f"Document {i+1} - {doc.get('title', 'Unknown')}\n{doc.get('content', '')[:500]}\n\n"

        prompt = (
            f"You are a helpful assistant. Use the context to answer the user's question.\n\n"
            f"Context:\n{context_text}\nUser Query: {query}"
        )
        if selected_text:
            prompt += f"\nUser highlighted: {selected_text}"

        try:
            response = openai.chat.completions.create(
                model=self.gpt_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"❌ GPT error: {e}")
            return "I'm sorry, I couldn't generate a response."

    async def chat(
        self,
        query: str,
        top_k: int = 5,
        selected_text: Optional[str] = None,
        session_id: Optional[str] = None   # <-- added session support
    ):
        logger.info(f"🔥 CHAT QUERY: {query}")
        context_docs = self.retrieve_context(query, top_k, selected_text)
        response_text = self.generate_response(query, context_docs, selected_text)
        return {
            "response": response_text,
            "context_docs": context_docs,
            "query": query,
            "selected_text": selected_text,
            "session_id": session_id
        }
