# Implementation Plan: Integrated RAG Chatbot for Published Book

## Technical Context

### Architecture Overview
- **Frontend**: Web book reader with floating chatbot toggle
- **Backend**: FastAPI with agent orchestration
- **LLM**: Google Gemini API for inference
- **Agent Framework**: OpenAI Agent SDK for orchestration
- **Vector Database**: Qdrant Cloud (Free Tier)
- **Relational Database**: Neon Serverless Postgres
- **Communication**: REST API with JSON payloads

### System Components
- **Book Reader UI**: Static/Dynamic content display with text selection
- **Chatbot Widget**: Floating toggle interface with conversation history
- **Backend API**: FastAPI endpoints for ingestion, retrieval, and chat
- **RAG Engine**: Retrieval and generation orchestration
- **Vector Store**: Book content embeddings with metadata
- **Session Store**: Conversation history and user context

### Unknowns (NEEDS CLARIFICATION)
- Specific book content format and structure
- Exact Gemini API model version to use
- OpenAI Agent SDK integration specifics with Gemini
- Qdrant indexing strategy for book-specific metadata

## Constitution Check

### Alignment Verification
- ✅ Follows RAG architecture principles
- ✅ Uses specified technology stack
- ✅ Maintains grounding in book content
- ✅ Implements proper security boundaries
- ✅ Enables text selection functionality
- ✅ Provides source attribution

### Gate Evaluation
- ✅ All specified technologies are available
- ✅ Architecture supports required functionality
- ✅ Security boundaries are properly defined
- ✅ Data flow respects content constraints

## Phase 0: Research & Resolution

### Research Tasks
1. **Gemini API Integration**: Research best practices for using Gemini API with FastAPI backend
2. **OpenAI Agent SDK with Gemini**: Investigate patterns for using OpenAI Agent SDK with non-OpenAI LLMs
3. **Qdrant Book Content Indexing**: Best practices for indexing book content with chapter/section metadata
4. **Text Selection Detection**: Methods for detecting and capturing text selections in web readers
5. **Floating Chatbot UI Patterns**: Best practices for embedded chatbot interfaces

### Expected Outcomes
- Clear integration approach for Gemini with FastAPI
- Agent orchestration strategy validated
- Vector indexing strategy defined
- Text selection capture mechanism identified
- UI interaction patterns established

## Phase 1: Design & Contracts

### Data Model Design
#### Core Entities
- **DocumentChunk**
  - id: string
  - content: string (500-1000 tokens)
  - embedding: float[] (768 dimensions for Gemini)
  - metadata: object
    - chapter: string
    - section: string
    - page: number
    - source_url: string
  - created_at: timestamp

- **Conversation**
  - id: string
  - user_id: string (optional)
  - created_at: timestamp
  - updated_at: timestamp

- **Message**
  - id: string
  - conversation_id: string
  - role: "user" | "assistant"
  - content: string
  - sources: DocumentChunk[]
  - selected_text: string (optional)
  - created_at: timestamp

### API Contract Design

#### Ingestion API
```
POST /ingest
Content-Type: application/json

{
  "documents": [
    {
      "content": "string",
      "metadata": {
        "chapter": "string",
        "section": "string",
        "page": "number",
        "source_url": "string"
      }
    }
  ]
}

Response: 200 OK
{
  "status": "processed",
  "chunks_created": number
}
```

#### Retrieval API
```
POST /retrieve
Content-Type: application/json

{
  "query": "string",
  "top_k": 5,
  "selected_text": "string" (optional)
}

Response: 200 OK
{
  "query": "string",
  "results": [
    {
      "id": "string",
      "content": "string",
      "metadata": {
        "chapter": "string",
        "section": "string",
        "page": "number",
        "source_url": "string"
      },
      "score": float
    }
  ]
}
```

#### Chat API
```
POST /chat
Content-Type: application/json

{
  "query": "string",
  "selected_text": "string" (optional),
  "conversation_history": [
    {
      "role": "user|assistant",
      "content": "string"
    }
  ],
  "session_id": "string" (optional),
  "top_k": 5
}

Response: 200 OK
{
  "response": "string",
  "sources": [
    {
      "id": "string",
      "title": "string",
      "url": "string",
      "score": float
    }
  ],
  "confidence": float,
  "selected_text_used": boolean,
  "session_id": "string"
}
```

#### Health Check API
```
GET /health

Response: 200 OK
{
  "status": "healthy",
  "message": "RAG Chatbot API is operational"
}
```

## Phase 2: Implementation Milestones

### Milestone 1: Data Ingestion Pipeline
**Duration**: 3-4 days
**Objective**: Establish content ingestion and vector storage

**Tasks**:
- Set up Qdrant Cloud connection
- Implement document chunking (500-1000 tokens)
- Create embedding generation using Gemini
- Build ingestion API endpoint
- Implement metadata enrichment
- Add duplicate detection and prevention

**Acceptance Criteria**:
- Books can be ingested in various formats
- Content properly chunked and embedded
- Vector storage populated with metadata
- Health checks pass

### Milestone 2: Retrieval Engine
**Duration**: 4-5 days
**Objective**: Implement semantic search and context retrieval

**Tasks**:
- Implement query embedding generation
- Build vector similarity search
- Create context retrieval with metadata
- Implement selected-text override logic
- Add confidence scoring
- Build retrieval API endpoint

**Acceptance Criteria**:
- Relevant content retrieved for queries
- Selected-text mode overrides global search
- Proper source attribution included
- Response time under 1 second

### Milestone 3: Chat Interface
**Duration**: 5-6 days
**Objective**: Create conversational interface with grounding

**Tasks**:
- Build FastAPI chat endpoint
- Integrate agent orchestration with OpenAI SDK
- Implement Gemini-powered response generation
- Add conversation history management
- Create response formatting with sources
- Implement grounding validation

**Acceptance Criteria**:
- Natural conversation flow maintained
- Responses grounded in book content
- Source attribution provided
- Selected-text context respected

### Milestone 4: Frontend Integration
**Duration**: 4-5 days
**Objective**: Embed chatbot in book reader with text selection

**Tasks**:
- Create floating chatbot UI component
- Implement text selection detection
- Build chat history display
- Add source citation formatting
- Create seamless book reader integration
- Implement responsive design

**Acceptance Criteria**:
- Chatbot accessible via floating toggle
- Text selection captured and sent
- Responses displayed with sources
- UI works across device sizes

### Milestone 5: Validation & Deployment
**Duration**: 3-4 days
**Objective**: Validate grounding and deploy to production

**Tasks**:
- Implement grounding validation checks
- Build accuracy testing framework
- Create deployment pipeline
- Add monitoring and logging
- Perform load testing
- Validate content constraints

**Acceptance Criteria**:
- <1% hallucination rate achieved
- Content constraint validation passes
- System handles expected load
- Production deployment successful

## Validation Checkpoints

### Grounding Validation
- **Metric**: Percentage of responses containing only book-sourced information
- **Target**: >95% book-sourced content
- **Method**: Automated content analysis against book corpus

### Accuracy Validation
- **Metric**: Correctness of responses to factual questions
- **Target**: >90% accuracy on test questions
- **Method**: Manual validation of sample queries

### Performance Validation
- **Metric**: Response time and system availability
- **Target**: <3 second response time, 99.9% uptime
- **Method**: Load testing and monitoring

### Content Constraint Validation
- **Metric**: Percentage of responses that include external knowledge
- **Target**: <1% external knowledge inclusion
- **Method**: Automated detection of non-book content

## Key Risks & Mitigations

### Risk 1: Gemini API Rate Limits
**Impact**: Degraded user experience during high traffic
**Mitigation**:
- Implement request queuing and retry logic
- Add client-side rate limiting
- Cache common queries and responses
- Monitor API usage and scale appropriately

### Risk 2: Qdrant Free Tier Limitations
**Impact**: Storage or query limits affecting functionality
**Mitigation**:
- Optimize vector storage and queries
- Implement data retention policies
- Monitor usage against tier limits
- Plan upgrade path if needed

### Risk 3: Content Grounding Failures
**Impact**: Hallucinated responses damaging credibility
**Mitigation**:
- Strict context window enforcement
- Multiple validation layers
- Confidence scoring and thresholding
- Regular testing and monitoring

### Risk 4: Text Selection Integration Complexity
**Impact**: Selected-text mode not functioning properly
**Mitigation**:
- Early prototype and testing
- Multiple selection detection methods
- Fallback mechanisms
- Cross-browser compatibility testing

### Risk 5: Agent SDK Compatibility Issues
**Impact**: OpenAI Agent SDK not working with Gemini
**Mitigation**:
- Early integration testing
- Fallback to direct API calls
- Alternative agent frameworks ready
- Close monitoring of SDK updates

## Success Criteria

### Technical Success
- End-to-end frontend-to-backend data flow operational
- All API endpoints responding correctly
- Chatbot providing grounded responses
- Text selection functionality working
- Source attribution accurate and complete

### Functional Success
- Users can ask questions about book content
- Responses consistently sourced from book
- Selected-text mode functions as expected
- System handles concurrent users
- Performance meets defined targets

### Quality Success
- Hallucination rate below 1%
- Content constraint validation passing
- User satisfaction above 90%
- System reliability at 99.9%
- Response quality meeting expectations