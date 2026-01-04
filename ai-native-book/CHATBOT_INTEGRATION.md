# AI Chatbot Integration

This Docusaurus-based textbook features an integrated AI chatbot that provides interactive learning capabilities through a floating toggle interface.

## Features

- **Floating UI**: A chat button that appears on all pages in the bottom-right corner
- **Text Selection**: Automatically detects selected text for context-aware responses
- **Session Management**: Maintains conversation history
- **Source Attribution**: Shows sources for generated responses
- **Confidence Scoring**: Provides confidence levels for answers
- **RAG Integration**: Uses Retrieval-Augmented Generation to answer questions about book content

## Architecture

### Frontend
- **Component**: `src/components/Chatbot/Chatbot.jsx`
- **Styling**: CSS Module with responsive design
- **Integration**: Global layout wrapper (`src/theme/Layout/index.js`)
- **API Connection**: Configurable via environment variables

### Backend
- **API Server**: FastAPI backend in `/backend/api/main.py`
- **Services**:
  - Google Gemini for embeddings and response generation
  - Qdrant for vector storage
  - Neon Postgres for chat history

## Setup Instructions

### 1. Start the Backend Server

```bash
cd backend
python -m uvicorn api.main:app --reload --port 8001
```

### 2. Start the Docusaurus Frontend

```bash
cd ai-native-book
npm start
```

### 3. Configure API Connection

The frontend connects to the backend via the environment variable in `.env`:

```
REACT_APP_API_BASE_URL=http://localhost:8001
```

## Usage

1. Click the 💬 button in the bottom-right corner to open the chat interface
2. Select text on the page to provide context (optional)
3. Type your question in the input field
4. Press Enter or click Send to get a response
5. The chatbot will use both your question and any selected text as context

## Development

### Adding the Chatbot to Custom Pages

The chatbot is automatically added to all pages via the Layout wrapper. If you want to add it to specific pages only, you can import and use the component directly:

```jsx
import Chatbot from '@site/src/components/Chatbot';

// Then in your component:
<Chatbot />
```

### Environment Variables

- `REACT_APP_API_BASE_URL`: Backend API URL (default: http://localhost:8001)

## Troubleshooting

- **Chatbot not appearing**: Ensure the Layout wrapper is properly implemented
- **API connection errors**: Check that the backend server is running and URL is correct
- **Text selection not working**: Verify that the mouseup event listener is active
- **Build errors**: Ensure all dependencies are installed (`npm install`)

## Files Added

- `src/components/Chatbot/` - Chatbot component and styling
- `src/theme/Layout/index.js` - Global layout wrapper
- `docs/chatbot-integration.md` - Documentation page
- `docs/chapter1/index.md` - Updated with chatbot usage instructions
- `sidebars.js` - Added chatbot documentation to sidebar
- `.env` - Environment configuration