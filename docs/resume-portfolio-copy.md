# Agent OS Resume and Portfolio Copy

## Resume Bullets

- Built Agent OS, a full-stack multi-agent orchestration platform that routes user tasks through supervisor, specialist, and critic agents with shared memory, permissions, workflow state, and execution traces.
- Implemented a modular FastAPI backend with typed Pydantic schemas, LangGraph-ready orchestration, permission-aware tools, Gemini provider support, local persistence, and document/CSV ingestion.
- Designed a Next.js and TypeScript dashboard for task submission, runtime provider validation, agent trace inspection, shared memory review, and final artifact download.
- Added research document ingestion for PDF, DOCX, Markdown, and text uploads, enabling agents to ground summaries in user-provided context.
- Created demo-ready sample tasks, mock datasets, architecture documentation, and a crash-course PDF to explain the system design and product motivation.

## Portfolio Project Description

Agent OS is a production-style MVP for a multi-agent AI workflow platform. Instead of exposing a single chatbot interface, it treats AI work as a coordinated system: a supervisor classifies the task, routes work to the correct specialist agent, persists shared memory, enforces permissions, records execution traces, sends outputs through a critic, and returns a final artifact.

The project demonstrates how agentic applications can become more inspectable and trustworthy by making state, routing, memory, and review visible to the user. It supports research tasks, planning tasks, CSV analysis, and uploaded document ingestion for research workflows.

## Short Pitch

Agent OS is an operating-system layer for AI agents. Users submit a task, the system routes it across specialized agents, tracks memory and state, enforces tool permissions, reviews the result, and shows the full execution trace in a dashboard.

## Technical Stack

- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, Python, Pydantic
- Agent architecture: supervisor-based routing, specialist agents, critic agent
- Orchestration: LangGraph-ready graph runner with fallback
- LLM provider: Gemini through a provider abstraction
- Storage: local JSON-backed task store with an upgrade path to Postgres
- Tools: permission-aware context reader, CSV profiler, document ingestion

## Demo Script

1. Open the dashboard and show the provider badge.
2. Submit a research task with an uploaded PDF, DOCX, Markdown, or text brief.
3. Show how the supervisor routes the task to the research agent and critic.
4. Open the workflow trace to show agent execution order and timestamps.
5. Open shared memory to show the uploaded document ingestion entry and extracted facts.
6. Show the final merged output and download links.
7. Switch to the CSV demo and upload `demo-data/sales_pipeline.csv`.
8. Show how the data agent profiles rows, columns, sample values, and next steps.

## Honest Limitations

- The current task store is local JSON, not Postgres.
- Background execution uses FastAPI background tasks, not a durable queue.
- Research is grounded in uploaded/local context, not live web search yet.
- The graph layer is ready for richer LangGraph flows, but retry and self-replanning loops are still future work.

## Strong Next Steps

- Add live web research with citations.
- Add Postgres persistence and queue-backed execution.
- Add streaming trace updates.
- Add auth and multi-project workspaces.
- Add richer retrieval over uploaded documents.
