import google.generativeai as genai  # type: ignore
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
from backend.rag.embeddings import EmbeddingGenerator
from backend.qdrant.vector_db import VectorDB
from backend.db.chat_history import ChatHistoryDB

# Load environment variables
load_dotenv()

class RetrievalAgent:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db
        self.embedding_generator = EmbeddingGenerator()
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        # Use the Gemini 2.0 Flash model
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat_history_db = ChatHistoryDB()

    def retrieve_context(self, query: str, top_k: int = 5, selected_text: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents based on the query
        If selected_text is provided, prioritize it in the search
        """
        if selected_text:
            # If selected text is provided, create embeddings for both the query and selected text
            query_embedding = self.embedding_generator.generate_query_embedding(query)
            selected_text_embedding = self.embedding_generator.generate_query_embedding(selected_text)

            # First, search for documents similar to the selected text
            selected_text_results = self.vector_db.search_documents(selected_text_embedding, limit=top_k)

            # Then, search for documents similar to the query
            query_results = self.vector_db.search_documents(query_embedding, limit=top_k)

            # Combine and deduplicate results, prioritizing those from selected text search
            combined_results = []
            seen_ids = set()

            # Add results from selected text search first (higher priority)
            for result in selected_text_results:
                if result['id'] not in seen_ids:
                    combined_results.append(result)
                    seen_ids.add(result['id'])

            # Add results from query search
            for result in query_results:
                if result['id'] not in seen_ids:
                    combined_results.append(result)
                    seen_ids.add(result['id'])

            # Return top_k results after deduplication
            return combined_results[:top_k]
        else:
            query_embedding = self.embedding_generator.generate_query_embedding(query)
            results = self.vector_db.search_documents(query_embedding, limit=top_k)
            return results

    def generate_response(self, query: str, context_docs: List[Dict[str, Any]], selected_text: Optional[str] = None) -> str:
        """
        Generate a response using Gemini with retrieved context
        """
        # Format context for the prompt with source information
        context_text = ""
        for i, doc in enumerate(context_docs):
            source_info = doc.get('url', 'Unknown source')
            if doc.get('title'):
                source_info = f"{doc.get('title', 'Unknown title')} ({source_info})"
            context_text += f"Document {i+1} - Source: {source_info}\n{doc['content'][:500]}...\n\n"

        # Create the message with context
        prompt = f"""You are a helpful assistant for robotics and AI topics.
        Use the following context to answer the user's question.
        If the context doesn't contain relevant information, say so.
        Always cite your sources from the provided context.

        Context:
        {context_text}

        User query: {query}"""

        # If selected text is provided, add it to the context
        if selected_text:
            prompt += f"\n\nAdditionally, the user has selected this specific text: {selected_text}"

        try:
            # Generate response using Gemini model
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            # If Gemini API call fails, create a contextual response from the documents
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                # Handle quota/rate limit errors specifically
                print(f"Quota error: {error_msg}")
                # Create a summary from the context documents
                if context_docs:
                    # Extract key information from the context to create a helpful response
                    content_snippets = [doc['content'][:300] for doc in context_docs if doc.get('content')]
                    combined_content = " ".join(content_snippets)
                    fallback_response = f"Based on the documents I found:\n\n{combined_content}\n\nFor more detailed answers, please ensure the API has proper quota allocation."
                else:
                    fallback_response = f"I found no relevant documents to answer your query: '{query}'. Please try a different question."
            else:
                # For other errors
                print(f"Gemini API error: {error_msg}")
                fallback_response = f"I'm sorry, but I'm currently unable to connect to the language model. Here's what I found in the documents:\n\n{context_text}\n\nBased on this, I cannot provide a detailed answer to your query: '{query}'. Please check your Gemini API configuration."
            return fallback_response

    async def query(self, user_query: str, top_k: int = 5, selected_text: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete query pipeline: retrieve context and generate response
        """
        # If session_id is provided, we could potentially retrieve context from the session
        # For now, just proceed with the normal query
        if session_id:
            try:
                db_session = await self.chat_history_db.get_session(session_id)
                if db_session:
                    # We could use session context here if needed
                    pass
            except Exception as e:
                print(f"Error loading session from database: {str(e)}")

        # Retrieve relevant documents
        context_docs = self.retrieve_context(user_query, top_k, selected_text=selected_text)

        # Calculate confidence based on the scores of the retrieved documents
        confidence = 0.0
        if context_docs:
            avg_score = sum(doc.get('score', 0) for doc in context_docs) / len(context_docs)
            # Normalize the score to 0-1 range (assuming Qdrant scores are cosine similarity)
            confidence = min(1.0, max(0.0, avg_score))

        # Generate response based on context
        response = self.generate_response(user_query, context_docs, selected_text=selected_text)

        # Extract sources from context docs
        sources = []
        for doc in context_docs:
            source_info = {
                "id": doc.get('id'),
                "title": doc.get('title', 'Unknown title'),
                "url": doc.get('url', 'Unknown source'),
                "score": doc.get('score', 0)
            }
            sources.append(source_info)

        return {
            "response": response,
            "context_docs": context_docs,
            "query": user_query,
            "selected_text": selected_text,
            "session_id": session_id,
            "confidence": confidence,
            "sources": sources
        }

    async def chat_with_history(self, user_query: str, conversation_history: List[Dict[str, str]], top_k: int = 5, selected_text: Optional[str] = None, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Chat with history, incorporating conversation context
        """
        # If session_id is provided, load conversation history from database
        if session_id:
            try:
                db_session = await self.chat_history_db.get_session(session_id)
                if db_session:
                    conversation_history = db_session["conversation_history"]
                else:
                    # Create new session if it doesn't exist
                    await self.chat_history_db.create_session(session_id)
            except Exception as e:
                print(f"Error loading session from database: {str(e)}")
                # Fallback to provided conversation history

        # Retrieve relevant documents based on current query
        context_docs = self.retrieve_context(user_query, top_k, selected_text=selected_text)

        # Calculate confidence based on the scores of the retrieved documents
        confidence = 0.0
        if context_docs:
            avg_score = sum(doc.get('score', 0) for doc in context_docs) / len(context_docs)
            # Normalize the score to 0-1 range (assuming Qdrant scores are cosine similarity)
            confidence = min(1.0, max(0.0, avg_score))

        # Format context
        context_text = ""
        for i, doc in enumerate(context_docs):
            source_info = doc.get('url', 'Unknown source')
            if doc.get('title'):
                source_info = f"{doc.get('title', 'Unknown title')} ({source_info})"
            context_text += f"Document {i+1} - Source: {source_info}\n{doc['content'][:500]}...\n\n"

        # Create the full prompt with context
        prompt = f"""You are a helpful assistant for robotics and AI topics.
        Use the following context to answer the user's question.
        If the context doesn't contain relevant information, say so.
        Always cite your sources from the provided context.

        Context:
        {context_text}

        Conversation History:"""

        # Add conversation history to the prompt
        for msg in conversation_history:
            role = msg["role"]
            content = msg["content"]
            prompt += f"\n{role.capitalize()}: {content}"

        prompt += f"\nUser: {user_query}"

        # If selected text is provided, add it to the context
        if selected_text:
            prompt += f"\n\nAdditionally, the user has selected this specific text: {selected_text}"

        try:
            # Generate response using Gemini model
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7,
                )
            )
            response_text = response.text
        except Exception as e:
            # Handle API errors and create a contextual response
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                # Handle quota/rate limit errors specifically
                print(f"Quota error in chat: {error_msg}")
                # Create a summary from the context documents
                if context_docs:
                    # Extract key information from the context to create a helpful response
                    content_snippets = [doc['content'][:300] for doc in context_docs if doc.get('content')]
                    combined_content = " ".join(content_snippets)
                    response_text = f"Based on the documents I found:\n\n{combined_content}\n\nFor more detailed answers, please ensure the API has proper quota allocation."
                else:
                    response_text = f"I found no relevant documents to answer your query: '{user_query}'. Please try a different question."
            else:
                # For other errors
                print(f"Gemini API error in chat: {error_msg}")
                context_text = ""
                for i, doc in enumerate(context_docs):
                    source_info = doc.get('url', 'Unknown source')
                    if doc.get('title'):
                        source_info = f"{doc.get('title', 'Unknown title')} ({source_info})"
                    context_text += f"Document {i+1} - Source: {source_info}\n{doc['content'][:500]}...\n\n"
                response_text = f"I'm sorry, but I'm currently unable to connect to the language model. Here's what I found in the documents:\n\n{context_text}\n\nBased on this, I cannot provide a detailed answer to your query: '{user_query}'. Please check your Gemini API configuration."

        # Add the new messages to the conversation history
        updated_history = conversation_history.copy()
        updated_history.append({"role": "user", "content": user_query})
        updated_history.append({"role": "assistant", "content": response_text})

        # If session_id is provided, save updated conversation to database
        if session_id:
            try:
                await self.chat_history_db.update_session(session_id, updated_history)
            except Exception as e:
                print(f"Error saving session to database: {str(e)}")

        # Extract sources from context docs
        sources = []
        for doc in context_docs:
            source_info = {
                "id": doc.get('id'),
                "title": doc.get('title', 'Unknown title'),
                "url": doc.get('url', 'Unknown source'),
                "score": doc.get('score', 0)
            }
            sources.append(source_info)

        return {
            "response": response_text,
            "context_docs": context_docs,
            "query": user_query,
            "selected_text": selected_text,
            "session_id": session_id,
            "confidence": confidence,
            "sources": sources
        }