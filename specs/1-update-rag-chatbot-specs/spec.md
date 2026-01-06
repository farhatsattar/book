# Integrated RAG Chatbot for Published Book - Specification

## Feature Overview

A production-ready Retrieval-Augmented Generation (RAG) chatbot embedded in a published book platform that answers user questions using only book content with strict guardrails against hallucination and external knowledge.

## User Stories

### Primary User Story
As a reader of the published book, I want to ask questions about the book content and receive accurate answers sourced only from the book, so that I can better understand and learn from the material.

### Secondary User Stories
- As a reader, I want to highlight specific text and ask questions about that text exclusively, so that I can get detailed explanations of particular concepts.
- As a reader, I want to see source attribution for answers, so that I can reference the original content.
- As a reader, I want the system to clearly indicate when information is not found in the book, so that I know the limits of the system.

## System Architecture

### High-Level Architecture
```
[Frontend UI] <-> [FastAPI Gateway] <-> [RAG Engine] <-> [Qdrant Vector DB]
                                          ↓
                                    [Neon Postgres DB]
```

### Components
1. **Frontend UI**: Embedded chatbot widget with text selection capability
2. **FastAPI Gateway**: Stateless API layer handling requests/responses
3. **RAG Engine**: Core orchestration component managing retrieval and generation
4. **Qdrant Vector DB**: Stores embedded book content with metadata
5. **Neon Postgres DB**: Stores conversation history and user data

### Data Flow Architecture
- Book content is processed through ETL pipeline into vector embeddings
- Vector embeddings stored in Qdrant with chapter/section/page metadata
- User queries processed through retrieval (similarity search) and generation (LLM response)
- Conversation history maintained in Postgres for context continuity

## RAG Flow

### Standard Query Flow
1. User submits question
2. Query embedding generated using same model as document embeddings
3. Vector similarity search performed against Qdrant collection
4. Top K relevant documents retrieved (K=5 default)
5. Retrieved context combined with user query
6. LLM generates response constrained to book content only
7. Response returned with source attributions

### Selected-Text Flow
1. User highlights text and asks question
2. System ignores global retrieval and uses selected text as sole context
3. LLM generates response based only on selected text
4. Response returned with "Based on selected text" attribution

### Guardrail Enforcement
- External knowledge filter blocks any information not in retrieved context
- Selected-text mode overrides global retrieval completely
- Confidence scoring applied to responses
- "Not found in book" returned when insufficient context

## Technical Stack

### Backend
- **Framework**: FastAPI for high-performance API layer
- **LLM Orchestration**: OpenAI-compatible API with configurable models
- **Deployment**: Serverless containers with auto-scaling

### Data Layer
- **Vector Database**: Qdrant Cloud (Free Tier) with cosine similarity
- **Relational Database**: Neon Serverless Postgres for metadata
- **Embedding Model**: Consistent model for both document and query embeddings

### Frontend
- **Widget**: Floating chatbot UI with text selection detection
- **Communication**: REST API calls to backend services
- **State Management**: Client-side conversation context

## Data Pipeline

### Content Ingestion
1. **Text Extraction**: Raw book content extracted from source format
2. **Normalization**: Text cleaned, standardized, and prepared
3. **Semantic Chunking**: Content divided into 500-1000 token segments
4. **Metadata Enrichment**: Chapter, section, page, and URL information added
5. **Embedding Generation**: Vector embeddings created using configured model
6. **Vector Storage**: Embeddings stored in Qdrant with metadata

### Indexing Strategy
- Semantic search enabled with cosine similarity
- Metadata filtering for source attribution
- Incremental updates for content changes
- Duplicate detection and prevention

## Functional Requirements

### Core Requirements
1. **Content Constraint**: Responses must only use information from book content
2. **Source Attribution**: All responses must include chapter/section/page references
3. **Not Found Handling**: System must explicitly state "not found in the book" when appropriate
4. **Selected-Text Mode**: When text is highlighted, responses must rely exclusively on selected text
5. **Confidence Scoring**: Responses include confidence level based on context relevance

### API Requirements
1. **Query Endpoint**: Accepts user questions and optional selected text
2. **Session Management**: Maintains conversation history per user session
3. **Error Handling**: Graceful handling of API limits, timeouts, and failures
4. **Rate Limiting**: Prevents abuse while allowing legitimate usage

### UI Requirements
1. **Chat Widget**: Floating interface with minimal visual footprint
2. **Text Selection Detection**: Automatically detects and offers to use selected text
3. **Response Formatting**: Clean presentation with source citations
4. **Loading States**: Clear indication during processing

## Non-Functional Requirements

### Performance
- Response time under 3 seconds for 95% of queries
- Support for 100 concurrent users
- 99.9% uptime SLA

### Security
- No sensitive data stored in plain text
- API key management for LLM services
- Rate limiting to prevent abuse
- Input sanitization to prevent injection attacks

### Reliability
- Fallback responses when LLM unavailable
- Graceful degradation when vector DB unavailable
- Retry mechanisms for transient failures
- Monitoring and alerting for system health

## Success Criteria

### Quantitative Metrics
- 95% of queries answered with book-sourced information
- Less than 1% of responses containing hallucinated content
- 99% of queries return within 3 seconds
- 90% of users report satisfactory answer quality
- 0% of responses contain external knowledge not in book

### Qualitative Measures
- Users can successfully navigate to referenced content using source attributions
- Selected-text mode functions without pulling in external context
- System clearly indicates when information is not available in book
- Conversational flow feels natural and helpful
- Confidence indicators are meaningful to users

## Key Entities

### Data Models
- **DocumentChunk**: Book content segment with embedding, metadata, and source
- **Conversation**: User session with history and context
- **Query**: User input with timestamp and session association
- **Response**: Generated answer with sources, confidence, and session association

### Relationships
- One Conversation contains many Queries and Responses
- Many DocumentChunks contribute to one Response (via retrieval)
- One DocumentChunk belongs to one Book section

## Assumptions

1. Book content is available in digital format suitable for text extraction
2. Sufficient computational resources available for embedding generation
3. LLM API service provides reliable access within usage limits
4. Book content is structured with chapters/sections for proper attribution
5. User internet connectivity supports real-time API communication

## Constraints

1. **No External Knowledge**: System must not access information outside book content
2. **Qdrant Free Tier**: Storage and query limits of Qdrant Cloud Free Tier apply
3. **Serverless Statelessness**: No persistent server-side session state allowed
4. **OpenAI-Compatible API**: Must work with OpenAI API format or compatible alternatives
5. **Budget Limitations**: Solution must work within free tier constraints of all services

## Risks

### Technical Risks
- Vector DB query performance degradation with large content sets
- LLM API rate limiting affecting user experience
- Embedding model drift causing retrieval accuracy issues

### Business Risks
- User frustration with "not found" responses
- Misleading attribution when context is insufficient
- Hallucination despite guardrails affecting credibility

## Testing Strategy

### Unit Tests
- Embedding generation consistency
- Query parsing and validation
- Source attribution accuracy
- Confidence scoring algorithms

### Integration Tests
- End-to-end RAG pipeline
- Selected-text mode functionality
- API rate limiting and error handling
- Database connection and session management

### Acceptance Tests
- Content constraint validation (no external knowledge)
- Selected-text mode exclusivity
- Source attribution correctness
- Performance under load

### Edge Cases
- Empty or minimal selected text
- Very long user queries
- Malformed input handling
- Concurrent user sessions