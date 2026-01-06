# Research Findings: Integrated RAG Chatbot Implementation

## Decision: Gemini API Integration with FastAPI
**Rationale**: Using Google's Generative Language API with FastAPI backend provides reliable access to Gemini models with proper error handling and rate limiting.
**Alternatives considered**:
- Direct HTTP calls vs Google's Python SDK
- Gemini Pro vs Gemini Flash models
- Caching strategies for API calls

## Decision: OpenAI Agent SDK with Gemini Compatibility
**Rationale**: The OpenAI Agent SDK is not directly compatible with Gemini API. Instead, we'll implement agent-like orchestration patterns using standard Python libraries with Gemini as the LLM backend.
**Alternatives considered**:
- Using LangChain with Gemini integration
- Building custom agent orchestration
- Google's own agent frameworks

## Decision: Qdrant Book Content Indexing Strategy
**Rationale**: Using cosine similarity with 768-dimensional embeddings (matching Gemini's embedding model) and storing chapter/section/page metadata for proper attribution.
**Alternatives considered**:
- Different embedding dimensions
- Alternative similarity metrics
- Hierarchical indexing approaches

## Decision: Text Selection Detection Method
**Rationale**: Using JavaScript's window.getSelection() API with mouseup event listeners to capture selected text and integrate with the chatbot interface.
**Alternatives considered**:
- Range-based selection APIs
- Shadow DOM approaches
- Browser extension patterns

## Decision: Floating Chatbot UI Implementation
**Rationale**: Using React-based floating widget with CSS transforms and positioning for seamless integration with existing book reader.
**Alternatives considered**:
- Standalone popup windows
- Sidebar integration
- Overlay approaches

## Best Practices: FastAPI with LLM Integration
**Findings**:
- Use async/await patterns for non-blocking LLM calls
- Implement proper request/response validation
- Add comprehensive error handling
- Use middleware for authentication/logging

## Best Practices: Vector Database Optimization
**Findings**:
- Pre-compute embeddings during ingestion
- Use metadata filtering for precise retrieval
- Implement proper indexing strategies
- Monitor query performance metrics

## Integration Patterns: Frontend-Backend Communication
**Findings**:
- REST APIs with JSON payloads for simplicity
- WebSocket connections for real-time chat
- Proper CORS configuration for web readers
- Error boundary patterns for resilience