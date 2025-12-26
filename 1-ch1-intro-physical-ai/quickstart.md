# Quickstart Guide: Chapter 1 - Introduction to Physical AI

## Overview
This guide will help you set up and run the Physical AI & Humanoid Robotics textbook with Chapter 1 implementation. The project uses Docusaurus for the frontend and FastAPI for the RAG backend.

## Prerequisites
- Node.js 18+
- Python 3.9+
- Access to Qdrant Cloud (free tier)
- Access to Neon Postgres (free tier)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone [repository-url]
cd ai-native-book
```

### 2. Frontend Setup (Docusaurus)
```bash
# Navigate to the project root
cd ai-native-book

# Install dependencies
npm install

# Create the docs directory structure
mkdir -p docs/chapter1

# Create Chapter 1 content files
touch docs/chapter1/index.md
touch docs/chapter1/concepts.md
touch docs/chapter1/history.md
touch docs/chapter1/comparison.md
```

### 3. Backend Setup (FastAPI)
```bash
# Create backend structure
mkdir -p src/server/fastapi
cd src/server/fastapi

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart qdrant-client psycopg2-binary python-dotenv
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
QDRANT_URL=https://your-qdrant-cluster.qdrant.tech:6333
QDRANT_API_KEY=your-qdrant-api-key
NEON_DATABASE_URL=postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/dbname
```

### 5. Initialize Chapter 1 Content
```bash
# Run the Docusaurus development server
npm run start
```

### 6. Run the RAG Backend
```bash
# From src/server/fastapi directory
uvicorn main:app --reload --port 8000
```

## Chapter 1 Content Structure
The chapter content is organized in the `docs/chapter1/` directory:
- `index.md` - Main introduction to Physical AI
- `concepts.md` - Core Physical AI concepts
- `history.md` - History and evolution of Physical AI
- `comparison.md` - Physical AI vs Traditional AI

## RAG Integration
The RAG system is accessible through the chat interface on each chapter page. Questions about Chapter 1 content will be answered based only on the textbook material.

## Building for Production
```bash
# Build the Docusaurus site
npm run build

# The built site will be in the build/ directory
# Deploy the build/ directory contents to GitHub Pages
```

## Testing
```bash
# Run frontend tests
npm test

# Run backend tests
cd src/server/fastapi
python -m pytest
```