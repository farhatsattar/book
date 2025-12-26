# Data Model: Chapter 1 - Introduction to Physical AI

## Entities

### Chapter Content
- **id**: string (unique identifier for the chapter)
- **title**: string (e.g., "Introduction to Physical AI")
- **content**: string (markdown content of the chapter)
- **sections**: array of Section objects
- **learningObjectives**: array of strings (what learners should understand)
- **keyTerms**: array of KeyTerm objects
- **visualAids**: array of VisualAid objects
- **summary**: string (concise overview of main points)
- **createdAt**: timestamp
- **updatedAt**: timestamp

### Section
- **id**: string (unique identifier for the section)
- **title**: string (section heading)
- **content**: string (markdown content)
- **order**: integer (position within the chapter)

### KeyTerm
- **id**: string (unique identifier for the term)
- **term**: string (the technical term)
- **definition**: string (clear explanation of the term)
- **context**: string (where in the chapter this term appears)
- **relatedTerms**: array of strings (other related terms)

### VisualAid
- **id**: string (unique identifier for the visual aid)
- **type**: string (diagram, chart, illustration, image)
- **title**: string (caption for the visual aid)
- **description**: string (explanation of what the visual aid shows)
- **src**: string (path to the asset)
- **altText**: string (accessibility description)

### RAGContext
- **id**: string (unique identifier for the RAG context)
- **chapterId**: string (reference to the chapter)
- **contentFragment**: string (specific text fragment for RAG retrieval)
- **embedding**: array of numbers (vector representation of the content)
- **metadata**: object (additional information for retrieval)
- **createdAt**: timestamp

### UserQuestion
- **id**: string (unique identifier for the question)
- **userId**: string (identifier for the user, if available)
- **questionText**: string (the question asked by the user)
- **chapterId**: string (which chapter the question relates to)
- **selectedText**: string (if text was highlighted when asking)
- **timestamp**: timestamp

### ChatResponse
- **id**: string (unique identifier for the response)
- **questionId**: string (reference to the question)
- **responseText**: string (the response from the RAG system)
- **sourceReferences**: array of strings (which parts of the textbook were used)
- **confidenceScore**: number (0-1 confidence in the response)
- **timestamp**: timestamp

## Relationships

- Chapter Content 1 --- * Section (one chapter has many sections)
- Chapter Content 1 --- * KeyTerm (one chapter has many key terms)
- Chapter Content 1 --- * VisualAid (one chapter has many visual aids)
- Chapter Content 1 --- * RAGContext (one chapter has many RAG contexts)
- UserQuestion 1 --- 1 ChatResponse (one question has one response)
- UserQuestion 1 --- 1 Chapter Content (one question relates to one chapter)

## Validation Rules

- Chapter title must be 5-100 characters
- Chapter content must not exceed 10,000 characters per section
- Key terms must have definitions of 10-200 characters
- Visual aids must have alt text for accessibility
- RAG contexts must have valid embeddings
- User questions must be 5-500 characters
- Response confidence score must be between 0 and 1

## State Transitions

- Chapter Content: Draft → Review → Published → Archived
- RAGContext: Created → Indexed → Active → Expired