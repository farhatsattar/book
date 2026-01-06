# Quickstart Guide: Integrated RAG Chatbot

## Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend development)
- Google Cloud Platform account with Gemini API access
- Qdrant Cloud account
- Neon Serverless Postgres account

## Setup Instructions

### 1. Environment Configuration
```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and connection strings
```

### 2. Environment Variables
Create `.env` file with:
```
GEMINI_API_KEY=your_google_gemini_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_postgres_connection_string
```

### 3. Backend Setup
```bash
# Navigate to backend
cd backend

# Start the API server
uvicorn api.main:app --reload --port 8001
```

### 4. Frontend Setup
```bash
# Navigate to frontend
cd ai-native-book

# Install dependencies
npm install

# Start the development server
npm start
```

## API Usage

### 1. Ingest Book Content
```bash
curl -X POST http://localhost:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "content": "Book chapter content here...",
        "metadata": {
          "chapter": "Chapter 1",
          "section": "Introduction",
          "page": 1,
          "source_url": "https://book.example.com/chapter1"
        }
      }
    ]
  }'
```

### 2. Chat with the Bot
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this book about?",
    "selected_text": null,
    "conversation_history": [],
    "session_id": "session-123",
    "top_k": 5
  }'
```

### 3. Retrieve Documents
```bash
curl -X POST http://localhost:8001/retrieve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning concepts",
    "top_k": 5,
    "selected_text": null
  }'
```

## Frontend Integration

### 1. Embed Chatbot Widget
The chatbot widget is automatically integrated into the book reader interface. It appears as a floating toggle button in the bottom-right corner.

### 2. Text Selection Feature
Users can select text within the book content and click the chatbot to ask questions specifically about the selected text. The system will prioritize the selected text in its response.

## Key Endpoints

- `POST /ingest` - Ingest book content into vector database
- `POST /chat` - Chat with the RAG system
- `POST /retrieve` - Retrieve relevant documents
- `GET /health` - Health check

## Development Workflow

### Backend Development
1. Make changes to `backend/` files
2. Restart the server with `uvicorn api.main:app --reload`
3. Test endpoints using the API documentation at `http://localhost:8001/docs`

### Frontend Development
1. Make changes to `ai-native-book/` files
2. Changes automatically reload in browser
3. Test chatbot functionality in the book reader interface

## Troubleshooting

### Common Issues
1. **API Key Issues**: Verify GEMINI_API_KEY is set correctly
2. **Database Connection**: Check QDRANT_URL and NEON_DATABASE_URL
3. **CORS Errors**: Ensure proper configuration in FastAPI middleware

### Testing
Run the test suite to verify functionality:
```bash
cd backend
python -m pytest tests/
```