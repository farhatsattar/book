# Chatbot Integration

The AI-powered chatbot is integrated into this Docusaurus site as a floating toggle button that appears on all pages.

## Features

- **Floating UI**: A chat button that appears in the bottom-right corner of every page
- **Text Selection**: Automatically detects selected text and provides context-aware responses
- **Session Management**: Maintains conversation history
- **Source Attribution**: Shows sources for generated responses
- **Confidence Scoring**: Provides confidence levels for answers

## How to Use

1. Click the 💬 button in the bottom-right corner to open the chat interface
2. Select text on the page to provide context (optional)
3. Type your question in the input field
4. Press Enter or click Send to get a response
5. The chatbot will use both your question and any selected text as context

## Backend Requirements

The chatbot requires the backend API to be running:

```bash
# From the backend directory
cd backend
uvicorn api.main:app --reload
```

## Configuration

The frontend connects to the backend API via the environment variable in `.env`:

```
REACT_APP_API_BASE_URL=http://localhost:8000
```

## Troubleshooting

- If the chatbot doesn't respond, ensure the backend server is running
- Check browser console for any error messages
- Verify API URL configuration in `.env` file