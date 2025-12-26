# Data Model: Chapter 2 - Embodied Intelligence and Humanoid Robotics

## Entities

### Chapter Content
- **id**: string (unique identifier for the chapter)
- **title**: string (e.g., "Embodied Intelligence and Humanoid Robotics")
- **content**: string (markdown content of the chapter)
- **sections**: array of Section objects
- **learningObjectives**: array of strings (what learners should understand)
- **keyTerms**: array of KeyTerm objects
- **visualAids**: array of VisualAid objects
- **summary**: string (concise overview of main points)
- **references**: array of strings (bibliographic references)
- **caseStudies**: array of CaseStudy objects
- **createdAt**: timestamp
- **updatedAt**: timestamp

### Section
- **id**: string (unique identifier for the section)
- **title**: string (section heading)
- **content**: string (markdown content)
- **order**: integer (position within the chapter)
- **learningObjectives**: array of strings (specific objectives for this section)

### KeyTerm
- **id**: string (unique identifier for the term)
- **term**: string (the technical term)
- **definition**: string (clear explanation of the term)
- **context**: string (where in the chapter this term appears)
- **relatedTerms**: array of strings (other related terms)
- **chapterId**: string (reference to the chapter)

### VisualAid
- **id**: string (unique identifier for the visual aid)
- **type**: string (diagram, chart, illustration, image, video)
- **title**: string (caption for the visual aid)
- **description**: string (explanation of what the visual aid shows)
- **src**: string (path to the asset)
- **altText**: string (accessibility description)
- **sectionId**: string (which section this belongs to)

### RAGContext
- **id**: string (unique identifier for the RAG context)
- **chapterId**: string (reference to the chapter)
- **sectionId**: string (reference to the section)
- **contentFragment**: string (specific text fragment for RAG retrieval)
- **embedding**: array of numbers (vector representation of the content)
- **metadata**: object (additional information for retrieval, including source tracking)
- **createdAt**: timestamp

### CaseStudy
- **id**: string (unique identifier for the case study)
- **title**: string (title of the case study)
- **description**: string (brief description)
- **content**: string (detailed case study content)
- **robotType**: string (type of humanoid robot or embodied system)
- **applicationDomain**: string (where the system is applied)
- **keyLessons**: array of strings (key takeaways from the case study)
- **createdAt**: timestamp

### UserQuestion
- **id**: string (unique identifier for the question)
- **userId**: string (identifier for the user, if available)
- **questionText**: string (the question asked by the user)
- **chapterId**: string (which chapter the question relates to)
- **sectionId**: string (which section the question relates to, if applicable)
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
- Chapter Content 1 --- * CaseStudy (one chapter has many case studies)
- Section 1 --- * VisualAid (one section has many visual aids)
- Section 1 --- * KeyTerm (one section has many key terms)
- Chapter Content 1 --- * RAGContext (one chapter has many RAG contexts)
- UserQuestion 1 --- 1 ChatResponse (one question has one response)
- UserQuestion 1 --- 1 Chapter Content (one question relates to one chapter)
- UserQuestion 1 --- 0..1 Section (one question may relate to a specific section)

## Validation Rules

- Chapter title must be 5-100 characters
- Chapter content must not exceed 10,000 characters per section
- Key terms must have definitions of 10-200 characters
- Visual aids must have alt text for accessibility
- RAG contexts must have valid embeddings
- User questions must be 5-500 characters
- Response confidence score must be between 0 and 1
- Case studies must have at least one key lesson
- Section order must be unique within a chapter

## State Transitions

- Chapter Content: Draft → Review → Published → Archived
- RAGContext: Created → Indexed → Active → Expired
- CaseStudy: Proposed → Draft → Published → Archived