---
id: 0001
title: Add initial constitution for Physical AI & Humanoid Robotics
stage: constitution
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: default
command: /sp.constitution
labels: ["constitution", "initial-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

```text
/sp.constitution

Project Name: Physical AI & Humanoid Robotics — Essentials

Purpose:
Create a short, clean, professional AI-Native textbook based on the Physical AI & Humanoid Robotics course.
The book must serve as a fast, simple, high-quality learning resource built with a modern Docusaurus UI
and a fully integrated free-tier RAG chatbot.

Scope:
- 6 short chapters:
  1. Introduction to Physical AI
  2. Basics of Humanoid Robotics
  3. ROS 2 Fundamentals
  4. Digital Twin Simulation (Gazebo + Isaac)
  5. Vision-Language-Action Systems
  6. Capstone: Simple AI-Robot Pipeline
- Clean UI
- Free-tier friendly
- Lightweight embeddings

Core Principles:
- Simplicity
- Accuracy
- Minimalism
- Fast builds
- Free-tier architecture
- RAG answers ONLY from book text

Key Features:
- Docusaurus textbook
- RAG chatbot (Qdrant + Neon + FastAPI)
- Select-text → Ask AI
- Optional Urdu / Personalize features

Constraints:
- No heavy GPU usage
- Minimal embeddings

Success Criteria:
- Build success
- Accurate chatbot
- Clean UI
- Smooth GitHub Pages deployment

Generate full constitution.
```

## Response snapshot

```
New version: 0.1.0 (Initial creation)

Files flagged for manual follow-up:
*   .specify/templates/plan-template.md: Pending review for alignment with new principles.
*   .specify/templates/spec-template.md: Pending review for alignment with new principles.
*   .specify/templates/tasks-template.md: Pending review for alignment with new principles.
*   .specify/templates/commands/*.md: Skipped due to directory not found.

Suggested commit message:
docs: add constitution v0.1.0 (initial creation + core principles)
```

## Outcome

- ✅ Impact: Successfully generated and updated the project constitution based on user input.
- 🧪 Tests: No tests were run or added in this step.
- 📁 Files: One file was created/modified: .specify/memory/constitution.md
- 🔁 Next prompts: User will review the constitution and suggested commit message.
- 🧠 Reflection: The process was smooth, except for the unexpected absence of the `.specify/templates/commands/` directory, which meant the consistency check for command files had to be skipped.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.sh` script was not found, requiring manual PHR creation. The `.specify/templates/commands/` directory was also not found.
- Graders run and results (PASS/FAIL): Not applicable for this step.
- Prompt variant (if applicable): Not applicable.
- Next experiment (smallest change to try): Investigate the expected location and presence of `.specify/templates/commands/` and `create-phr.sh`.
