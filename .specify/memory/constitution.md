<!-- Sync Impact Report
Version change: 1.0.0 -> 1.1.0 (Scope update from 15 to 5 chapters)
List of modified principles:
- Simplicity over completeness → Simplicity over completeness
- Accuracy over speculation → Accuracy over speculation
- Minimalism over feature bloat → Minimalism over feature bloat
- Fast builds and deployments → Fast builds and deployments
- Free-tier-first architecture → Free-tier-first architecture
- RAG chatbot must answer ONLY from textbook content → RAG chatbot must answer ONLY from textbook content
Added sections: Updated 5-chapter scope
Removed sections: 10-15 chapter listings
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/*.md: Skipped (directory not found)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics — Essentials Constitution

## Core Principles

### Simplicity over completeness
The project prioritizes straightforward solutions, clear code, and an easy-to-understand user experience. Avoid unnecessary complexity. Focus on essential features that deliver maximum educational value with minimal overhead.

### Accuracy over speculation
All information presented in the textbook and provided by the RAG chatbot must be factually correct and derived directly from the book's content. No external knowledge or hallucinations are permitted. Content must be grounded in established Physical AI and robotics principles.

### Minimalism over feature bloat
Design and implementation should be lean, focusing on essential features to ensure a lightweight and efficient system. Every feature must justify its inclusion based on clear educational value and practical necessity.

### Fast builds and deployments
The Docusaurus build process must be optimized for speed to facilitate rapid iteration and deployment. Build times should remain under acceptable limits to support continuous development and updates.

### Free-tier-first architecture
All infrastructure and services used (e.g., Qdrant Cloud, Neon Serverless Postgres, FastAPI) must align with free-tier limitations to ensure accessibility and minimize operational costs. Architecture decisions must prioritize cost-effectiveness and sustainability.

### RAG chatbot must answer ONLY from textbook content
The RAG chatbot must strictly use the textbook's content as its sole source of truth for generating answers. No external knowledge, no hallucinations, no speculative responses - only information grounded in the provided chapters and sections.

## Scope and Key Features

**Scope:**
- An AI-native textbook consisting of 5 concise, well-structured chapters:
  1. Introduction to Physical AI
  2. Embodied Intelligence and Humanoid Robotics
  3. Sensors and Actuators in Physical AI
  4. ROS 2 and Robot Control Systems
  5. AI Perception and Action Integration

- Clean, professional Docusaurus-based UI
- Fully deployable on GitHub Pages
- Free-tier friendly system architecture
- Lightweight, minimal embeddings suitable for a textbook-sized corpus

**Key Features:**
- AI-Native textbook built with Docusaurus
- Embedded RAG chatbot using:
  - FastAPI backend
  - Qdrant Cloud (free tier) for vector storage and retrieval
  - Neon Serverless Postgres for metadata and document tracking
- Ability for users to select text and ask questions based strictly on that selection
- Source-grounded answers referencing chapters or sections
- Optional bonus features:
  - Urdu translation of chapters
  - Learner-level personalization based on background

## Constraints and Success Criteria

**Constraints:**
- No heavy GPU usage or local model training
- No paid-only infrastructure or proprietary lock-in
- Minimal, efficient embeddings
- No prompt-only or hallucination-prone chatbot behavior
- No static PDFs or non-interactive content
- Spec-driven development using Spec-Kit Plus
- Clear separation between specification and implementation

**Success Criteria:**
- Successful build and deployment on GitHub Pages
- Clean, readable, professional user interface
- Accurate, source-grounded RAG chatbot responses
- Smooth performance within free-tier limits
- Clear evidence of Spec-Kit Plus usage
- Alignment between constitution, specs, and implementation

## Governance

The Constitution outlines the foundational principles and guidelines for the "Physical AI & Humanoid Robotics — Essentials" project. All design, development, and deployment activities must adhere to these principles. Any proposed amendments to this Constitution require a formal review process, documentation of the rationale, and explicit approval from project stakeholders. Compliance with these rules will be regularly reviewed.

**Version**: 1.1.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-23