import asyncio
from backend.db.chat_history import ChatHistoryDB

async def initialize_database():
    """
    Initialize the database tables
    """
    chat_history_db = ChatHistoryDB()
    await chat_history_db.initialize_db()
    print("Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(initialize_database())