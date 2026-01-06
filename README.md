# Physical AI & Humanoid Robotics Textbook

Welcome to the Physical AI & Humanoid Robotics textbook - an AI-native educational resource with integrated RAG-powered chatbot functionality.

## Features

- Complete textbook on Physical AI and Humanoid Robotics
- Interactive AI chatbot with floating UI
- Text selection for context-aware responses
- Source attribution and confidence scoring
- RAG (Retrieval-Augmented Generation) integration

## Structure

- `ai-native-book/` - Docusaurus-based textbook with chatbot integration
- `backend/` - FastAPI backend for the RAG system
- `specs/` - Feature specifications and planning documents

## Getting Started

### Frontend (Docusaurus textbook)

1. Navigate to the textbook directory:
   ```bash
   cd ai-native-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Backend (RAG System)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Set up environment variables in `.env`:
   ```bash
   # Add your API keys
   GEMINI_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   QDRANT_API_KEY=your_key_here
   NEON_DATABASE_URL=your_database_url
   ```

3. Start the backend server:
   ```bash
   uvicorn api.main:app --reload
   ```

## Chatbot Integration

The textbook features an AI chatbot accessible via a floating button on all pages. The chatbot can:
- Answer questions about book content
- Use selected text as context for more relevant answers
- Provide source attribution and confidence scores
- Maintain conversation history

For more details about the chatbot integration, see `ai-native-book/CHATBOT_INTEGRATION.md`.

## Chapters

The textbook covers:
- Chapter 1: Introduction to Physical AI
- Chapter 2: Embodied Intelligence and Humanoid Robotics
- Chapter 3: Sensors and Actuators in Physical AI
- Chapter 4: ROS 2 and Robot Control Systems
- Chapter 5: AI Perception and Action Integration
