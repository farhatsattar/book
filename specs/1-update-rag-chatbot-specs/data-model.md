# Data Model: Integrated RAG Chatbot

## Core Entities

### DocumentChunk
**Description**: Represents a semantically meaningful segment of book content
- **id**: string (UUID) - Unique identifier for the chunk
- **content**: string - Text content (500-1000 tokens)
- **embedding**: number[] (length: 768) - Gemini-compatible embedding vector
- **metadata**: object
  - **chapter**: string - Chapter identifier from book
  - **section**: string - Section within chapter
  - **page**: number - Page number in original book
  - **source_url**: string - URL reference to original content
  - **book_id**: string - Identifier for the book this chunk belongs to
- **created_at**: ISO date string - Timestamp of creation
- **updated_at**: ISO date string - Timestamp of last update

**Relationships**: Belongs to one Book, referenced by many Messages

### Conversation
**Description**: Tracks a user's chat session with the system
- **id**: string (UUID) - Unique conversation identifier
- **user_id**: string (optional) - User identifier (if authenticated)
- **session_id**: string - Session identifier for anonymous users
- **created_at**: ISO date string - Session start time
- **updated_at**: ISO date string - Last activity time
- **active**: boolean - Whether session is currently active

**Relationships**: Contains many Messages

### Message
**Description**: Individual message in a conversation
- **id**: string (UUID) - Unique message identifier
- **conversation_id**: string - Foreign key to Conversation
- **role**: enum ("user"|"assistant") - Sender type
- **content**: string - Message text content
- **sources**: array of DocumentChunk references - Source documents used
- **selected_text**: string (optional) - Text that was selected by user (if applicable)
- **confidence**: number (0-1) - Confidence score for the response
- **created_at**: ISO date string - Timestamp of message creation

**Relationships**: Belongs to one Conversation, references many DocumentChunks

### Book
**Description**: Represents a book in the system
- **id**: string (UUID) - Unique book identifier
- **title**: string - Book title
- **author**: string - Book author(s)
- **isbn**: string (optional) - ISBN identifier
- **published_date**: ISO date string - Publication date
- **url**: string - URL to book location
- **chunk_count**: number - Total number of chunks in the book
- **created_at**: ISO date string - Ingestion time
- **updated_at**: ISO date string - Last update time

**Relationships**: Contains many DocumentChunks

### ChatHistory
**Description**: Stores conversation history for persistence
- **id**: string (UUID) - Unique history record identifier
- **conversation_id**: string - Foreign key to Conversation
- **message_sequence**: number - Order of message in conversation
- **message_id**: string - Foreign key to Message
- **created_at**: ISO date string - Record creation time

**Relationships**: Links Conversation and Message entities

## Validation Rules

### DocumentChunk Validations
- Content must be between 500-1000 tokens
- Embedding must be exactly 768 dimensions
- Metadata fields must be properly structured
- Book_id must reference existing Book

### Message Validations
- Role must be either "user" or "assistant"
- Content must not exceed 10,000 characters
- Confidence must be between 0 and 1
- Sources must reference valid DocumentChunks

### Conversation Validations
- Session_id must be provided if user_id is null
- Cannot have more than 1000 messages per conversation
- Must be associated with at least one Book

## State Transitions

### Conversation States
- **Created**: New conversation initiated
- **Active**: User actively chatting
- **Paused**: Inactivity timeout (15 min)
- **Closed**: Session explicitly ended
- **Archived**: Long-term storage after inactivity

### Message States
- **Pending**: Message received, processing
- **Generated**: Response created by LLM
- **Validated**: Response checked for accuracy
- **Delivered**: Sent to user interface
- **Confirmed**: User acknowledged receipt

## Indexing Strategy

### Qdrant Vector Collection
- **Collection Name**: `book_chunks`
- **Vector Size**: 768 (for Gemini embeddings)
- **Distance Metric**: Cosine similarity
- **Payload Fields**: chapter, section, page, book_id, source_url

### Neon Postgres Indices
- Conversation: index on (user_id, created_at)
- Message: index on (conversation_id, created_at)
- Book: index on (title, author)
- ChatHistory: index on (conversation_id, message_sequence)