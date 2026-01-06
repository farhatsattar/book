import asyncpg
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatHistoryDB:
    def __init__(self):
        self.connection_string = os.getenv("NEON_DATABASE_URL")
        if not self.connection_string:
            raise ValueError("NEON_DATABASE_URL environment variable is required")

    async def get_connection(self):
        """Get a database connection"""
        return await asyncpg.connect(dsn=self.connection_string)

    async def initialize_db(self):
        """Initialize the database tables"""
        conn = await self.get_connection()
        try:
            # Create chat_sessions table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    conversation_history JSONB DEFAULT '[]'
                )
            ''')

            # Create indexes
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_chat_sessions_user_id
                ON chat_sessions(user_id)
            ''')
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_chat_sessions_updated_at
                ON chat_sessions(updated_at)
            ''')
        finally:
            await conn.close()

    async def create_session(self, session_id: str, user_id: Optional[str] = None) -> Dict:
        """Create a new chat session"""
        conn = await self.get_connection()
        try:
            query = '''
                INSERT INTO chat_sessions (session_id, user_id, conversation_history)
                VALUES ($1, $2, $3)
                RETURNING session_id, user_id, created_at, updated_at, conversation_history
            '''
            result = await conn.fetchrow(
                query,
                session_id,
                user_id,
                json.dumps([])
            )
            return {
                "session_id": result["session_id"],
                "user_id": result["user_id"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
                "conversation_history": result["conversation_history"]
            }
        finally:
            await conn.close()

    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get a chat session by ID"""
        conn = await self.get_connection()
        try:
            query = '''
                SELECT session_id, user_id, created_at, updated_at, conversation_history
                FROM chat_sessions
                WHERE session_id = $1
            '''
            result = await conn.fetchrow(query, session_id)
            if result:
                return {
                    "session_id": result["session_id"],
                    "user_id": result["user_id"],
                    "created_at": result["created_at"],
                    "updated_at": result["updated_at"],
                    "conversation_history": result["conversation_history"]
                }
            return None
        finally:
            await conn.close()

    async def update_session(self, session_id: str, conversation_history: List[Dict]) -> Dict:
        """Update a chat session with new conversation history"""
        conn = await self.get_connection()
        try:
            query = '''
                UPDATE chat_sessions
                SET conversation_history = $1, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = $2
                RETURNING session_id, user_id, created_at, updated_at, conversation_history
            '''
            result = await conn.fetchrow(
                query,
                json.dumps(conversation_history),
                session_id
            )
            return {
                "session_id": result["session_id"],
                "user_id": result["user_id"],
                "created_at": result["created_at"],
                "updated_at": result["updated_at"],
                "conversation_history": result["conversation_history"]
            }
        finally:
            await conn.close()

    async def add_message_to_session(self, session_id: str, role: str, content: str) -> Dict:
        """Add a message to an existing session"""
        session = await self.get_session(session_id)
        if not session:
            # Create new session if it doesn't exist
            session = await self.create_session(session_id)

        conversation_history = session["conversation_history"]
        conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })

        return await self.update_session(session_id, conversation_history)

    async def get_all_sessions(self, user_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get all sessions for a user or all sessions if user_id is None"""
        conn = await self.get_connection()
        try:
            if user_id:
                query = '''
                    SELECT session_id, user_id, created_at, updated_at, conversation_history
                    FROM chat_sessions
                    WHERE user_id = $1
                    ORDER BY updated_at DESC
                    LIMIT $2
                '''
                results = await conn.fetch(query, user_id, limit)
            else:
                query = '''
                    SELECT session_id, user_id, created_at, updated_at, conversation_history
                    FROM chat_sessions
                    ORDER BY updated_at DESC
                    LIMIT $1
                '''
                results = await conn.fetch(query, limit)

            return [
                {
                    "session_id": r["session_id"],
                    "user_id": r["user_id"],
                    "created_at": r["created_at"],
                    "updated_at": r["updated_at"],
                    "conversation_history": r["conversation_history"]
                }
                for r in results
            ]
        finally:
            await conn.close()