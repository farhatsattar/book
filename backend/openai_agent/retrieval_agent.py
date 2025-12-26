import openai
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from ..rag.embeddings import EmbeddingGenerator
from ..qdrant.vector_db import VectorDB

# Load environment variables
load_dotenv()

class RetrievalAgent:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db
        self.embedding_generator = EmbeddingGenerator()
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents based on the query
        """
        query_embedding = self.embedding_generator.generate_query_embedding(query)
        results = self.vector_db.search_documents(query_embedding, limit=top_k)
        return results

    def generate_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        Generate a response using OpenAI with retrieved context
        """
        # Format context for the prompt
        context_text = "\n\n".join([
            f"Document {i+1}:\n{doc['content'][:500]}..."
            for i, doc in enumerate(context_docs)
        ])

        # Create the prompt with context
        system_prompt = f"""You are a helpful assistant for robotics and AI topics.
        Use the following context to answer the user's question.
        If the context doesn't contain relevant information, say so.

        Context:
        {context_text}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def query(self, user_query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Complete query pipeline: retrieve context and generate response
        """
        # Retrieve relevant documents
        context_docs = self.retrieve_context(user_query, top_k)

        # Generate response based on context
        response = self.generate_response(user_query, context_docs)

        return {
            "response": response,
            "context_docs": context_docs,
            "query": user_query
        }

    def chat_with_history(self, user_query: str, conversation_history: List[Dict[str, str]], top_k: int = 5) -> Dict[str, Any]:
        """
        Chat with history, incorporating conversation context
        """
        # Retrieve relevant documents based on current query
        context_docs = self.retrieve_context(user_query, top_k)

        # Format context
        context_text = "\n\n".join([
            f"Document {i+1}:\n{doc['content'][:500]}..."
            for i, doc in enumerate(context_docs)
        ])

        # Create system prompt with context
        system_prompt = f"""You are a helpful assistant for robotics and AI topics.
        Use the following context to answer the user's question.
        If the context doesn't contain relevant information, say so.

        Context:
        {context_text}"""

        # Prepare messages including conversation history
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current user query
        messages.append({"role": "user", "content": user_query})

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )

            return {
                "response": response.choices[0].message.content,
                "context_docs": context_docs,
                "query": user_query
            }
        except Exception as e:
            return {
                "response": f"Error generating response: {str(e)}",
                "context_docs": [],
                "query": user_query
            }