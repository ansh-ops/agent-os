# Agent OS

Agent OS is an execution-ready MVP for a multi-agent orchestration platform that behaves like an operating system for AI agents. A user submits a task, the supervisor classifies it, routes it to the right specialist agents, persists shared state, applies a permission model, records a human-readable execution trace, and publishes a final artifact.

## What the MVP demonstrates

- Multi-agent orchestration with a supervisor-first flow
- Graph-driven orchestration with a LangGraph execution layer and plain-Python fallback
- Research, planning, data, and critic agents with explicit roles
- Shared memory entries for task summary, extracted facts, agent outputs, execution events, and final artifacts
- Permission-aware agent capabilities represented in code
- Permission-aware tool execution for context and CSV access
- Research document ingestion for PDF, DOCX, Markdown, and text uploads
- Model-provider abstraction for optional live LLM-backed structured outputs
- Task lifecycle tracking from `queued` to `completed` or `failed`
- Visible workflow trace and final output in a clean Next.js dashboard
- Upgrade path to real LLM providers through clear backend interfaces

## Architecture

### Workflow diagram

```text
[User Task + Optional File]
          |
          v
[FastAPI Task API]
          |
          v
[Task Store] <----> [Shared Memory Store]
          |
          v
[Supervisor / Orchestrator]
   | classify task
   | select route
   | manage state
   | merge artifacts
   v
[Specialist Agent]
   | research_agent
   | planning_agent
   | data_agent
   v
[Critic Agent]
          |
          v
[Final Result + Execution Trace + Downloadable Artifacts]
          |
          v
[Next.js Dashboard]
```

### Architecture summary

Agent OS uses a supervisor-based orchestration model. The API creates a task record, the supervisor infers the workflow route, the LangGraph runner initializes the agent path, specialist agents use permission-scoped tools and optional model-backed structured generation, the critic agent reviews quality, and the system persists memory plus execution traces so the full run is visible in the UI.

### Backend

The backend is a FastAPI application with modular domains:

- [backend/app/api/routes.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/api/routes.py) exposes task APIs and file upload handling
- [backend/app/orchestration/supervisor.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/orchestration/supervisor.py) owns task classification, agent routing, orchestration order, and result merging
- [backend/app/orchestration/graph.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/orchestration/graph.py) provides the LangGraph workflow runner with a safe fallback
- [backend/app/agents](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/agents) contains specialist agents, typed output contracts, and isolated prompt/config files
- [backend/app/models/provider.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/models/provider.py) abstracts model-backed structured completion
- [backend/app/tools](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/tools) contains permission-aware tools used by specialist agents
- [backend/app/services/document_ingestion.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/services/document_ingestion.py) extracts research context from uploaded documents
- [backend/app/memory/store.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/memory/store.py) handles explicit shared memory writes
- [backend/app/permissions/roles.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/permissions/roles.py) defines the permission model
- [backend/app/state/store.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/state/store.py) persists task records via a local JSON-backed abstraction
- [backend/app/services/task_executor.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/services/task_executor.py) manages task creation and background execution
- [backend/app/schemas/task.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/schemas/task.py) contains typed Pydantic schemas for requests, responses, memory, traces, artifacts, and state

Agent prompt/configuration is intentionally isolated into dedicated files:

- [backend/app/agents/configs/research.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/agents/configs/research.py)
- [backend/app/agents/configs/planning.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/agents/configs/planning.py)
- [backend/app/agents/configs/data.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/agents/configs/data.py)
- [backend/app/agents/configs/critic.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/agents/configs/critic.py)

Structured agent outputs are defined in:

- [backend/app/agents/contracts.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/agents/contracts.py)

The local JSON store keeps the MVP easy to run while preserving a straightforward migration path to Postgres or Redis-backed infrastructure later.

### Frontend

The frontend is a Next.js App Router dashboard with focused views:

- [frontend/src/components/TaskSubmissionPanel.tsx](/Users/anshk/Desktop/Projectssss/Agent%20OS/frontend/src/components/TaskSubmissionPanel.tsx) submits new tasks and optional files
- [frontend/src/components/WorkflowView.tsx](/Users/anshk/Desktop/Projectssss/Agent%20OS/frontend/src/components/WorkflowView.tsx) shows orchestration state and trace entries
- [frontend/src/components/MemoryView.tsx](/Users/anshk/Desktop/Projectssss/Agent%20OS/frontend/src/components/MemoryView.tsx) surfaces shared memory
- [frontend/src/components/FinalOutputView.tsx](/Users/anshk/Desktop/Projectssss/Agent%20OS/frontend/src/components/FinalOutputView.tsx) renders the merged result and download links
- [frontend/src/components/TaskListSidebar.tsx](/Users/anshk/Desktop/Projectssss/Agent%20OS/frontend/src/components/TaskListSidebar.tsx) tracks recent workflows

The UI is intentionally dashboard-oriented rather than chat-oriented so the orchestration system stays visible.

## Folder structure

```text
agent-os/
  backend/
    app/
      api/
      agents/
      orchestration/
      memory/
      permissions/
      state/
      services/
      schemas/
      core/
    tests/
    requirements.txt
    Dockerfile
  frontend/
    src/
      app/
      components/
      lib/
      types/
    package.json
    Dockerfile
  demo-data/
  docker-compose.yml
  README.md
```

## Agent system

### Supervisor / Orchestrator

- Receives the task
- Infers task type when the user selects `auto`
- Chooses the specialist route
- Maintains workflow state
- Merges outputs into final sections and downloadable artifacts
- Owns retries, trace entries, and shared memory coordination

### Research Agent

- Reads text context and uploaded research documents
- Extracts findings
- Produces a structured research summary

### Data Agent

- Reads uploaded CSV files
- Profiles columns, row counts, and basic numeric ranges
- Suggests issues and next analysis steps

### Planning Agent

- Turns goals into implementation phases and tasks
- Produces project-style execution structures

### Critic Agent

- Reviews prior output only
- Flags weak spots and recommends approval or refinement

Each agent has a narrow interface: it receives `AgentContext` and returns an `AgentResult` with a typed `structured_output`. That keeps the orchestration layer readable, modular, and easy to extend with future agents.

Each specialist agent can also run in two modes:

- Local-first deterministic mode for reliable demos
- Model-backed structured mode when a provider is configured

## Permission model

The permission model is intentionally simple and explicit:

- `research_agent`: `read_context`, `write_memory`
- `data_agent`: `read_csv`, `write_memory`
- `planning_agent`: `read_context`, `read_agent_outputs`, `write_memory`
- `critic_agent`: `read_agent_outputs`, `review_outputs`
- `supervisor`: full coordination access

This lives in [backend/app/permissions/roles.py](/Users/anshk/Desktop/Projectssss/Agent%20OS/backend/app/permissions/roles.py), making future RBAC expansion straightforward.

## Task lifecycle

Supported workflow states:

- `queued`
- `planning`
- `running`
- `waiting_on_agent`
- `under_review`
- `completed`
- `failed`

## Example flows

### Flow 1: Research

Use the prompt:

`Research AI agent operating systems and summarize the strongest MVP patterns.`

Optional context:

`Use the local technical brief and focus on orchestration, memory, and visibility.`

Route:

`supervisor -> research_agent -> critic_agent`

### Flow 2: Planning

Use the prompt:

`Plan a two-week implementation roadmap for an internal AI analyst tool.`

Route:

`supervisor -> planning_agent -> critic_agent`

### Flow 3: Data

Upload [demo-data/sales_pipeline.csv](/Users/anshk/Desktop/Projectssss/Agent%20OS/demo-data/sales_pipeline.csv) and use the prompt:

`Analyze this CSV and suggest the most important next actions for sales operations.`

Route:

`supervisor -> data_agent -> critic_agent`

## Demo assets

The repo includes immediate demo content:

- [demo-data/sample_tasks.json](/Users/anshk/Desktop/Projectssss/Agent%20OS/demo-data/sample_tasks.json) with ready-to-use prompts
- [demo-data/sales_pipeline.csv](/Users/anshk/Desktop/Projectssss/Agent%20OS/demo-data/sales_pipeline.csv) for the data flow
- [demo-data/technical-brief-source.txt](/Users/anshk/Desktop/Projectssss/Agent%20OS/demo-data/technical-brief-source.txt) for research-style context
- [docs/resume-portfolio-copy.md](/Users/anshk/Desktop/Projectssss/Agent%20OS/docs/resume-portfolio-copy.md) with resume bullets, portfolio copy, and a demo script

The dashboard also includes preset quick-start tasks in [frontend/src/lib/sampleTasks.ts](/Users/anshk/Desktop/Projectssss/Agent%20OS/frontend/src/lib/sampleTasks.ts), so the app is demo-ready immediately after setup.

## Local development

### Option 1: Run with Docker

```bash
docker compose up --build
```

Frontend:

[http://localhost:3000](http://localhost:3000)

Backend:

[http://localhost:8000/docs](http://localhost:8000/docs)

### Option 2: Run services directly

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

### Environment variables

Copy [.env.example](/Users/anshk/Desktop/Projectssss/Agent%20OS/.env.example) to `.env` if you want to customize values.

- `NEXT_PUBLIC_API_BASE_URL`: frontend API target
- `LLM_PROVIDER`: provider selector, defaults to `gemini`
- `GEMINI_API_KEY`: enables model-backed structured agent execution with Gemini
- `OPENAI_API_KEY`: optional alternate provider key if you switch `LLM_PROVIDER`
- `USE_MOCK_AGENTS`: set to `false` to prefer the configured model provider

## API overview

- `POST /api/tasks`
- `GET /api/tasks`
- `GET /api/tasks/{task_id}`
- `GET /api/tasks/{task_id}/download?format=text|json`
- `GET /health`

## Extending with real models later

The current agents work in two modes:

- Local-first fallback mode for deterministic demos
- Model-backed mode when `GEMINI_API_KEY` is set, `LLM_PROVIDER=gemini`, and `USE_MOCK_AGENTS=false`

To upgrade further:

1. Replace the specialist `run()` implementations with LangGraph nodes or model-backed services.
2. Move the local task store to Postgres while keeping the existing schema shapes.
3. Add retrieval, embeddings, and external tools behind the permission layer.
4. Introduce Redis or a queue if task volume or concurrency increases.

## Future improvements

- Real asynchronous job queue and streaming trace updates
- LangGraph-native graph visualization and step retries
- Better data analysis with chart artifacts and richer statistics
- Memory search and artifact versioning
- Human-in-the-loop approvals for sensitive tool usage
- Authentication, multi-project workspaces, and team collaboration

## Build summary

### What was built

- A modular FastAPI backend with supervisor-based multi-agent orchestration
- Separate research, planning, data, and critic agents with isolated configs
- LangGraph-ready workflow orchestration with a plain fallback runner
- Permission-aware tool abstractions for context and CSV operations
- Model-provider abstraction for optional live LLM-backed structured outputs
- Shared memory, role-based permissions, workflow states, and execution traces
- A Next.js dashboard for task submission, workflow inspection, memory viewing, and final artifact review
- Dockerized local setup, sample tasks, and bundled mock data for immediate demos

### What is mocked

- Agent intelligence falls back to deterministic heuristics unless a real model provider is configured
- Task execution runs in FastAPI background tasks instead of a durable queue
- The local JSON store stands in for Postgres and Redis-style infrastructure
- Tooling is still intentionally narrow and does not yet include real web retrieval, code execution, or broad external integrations

### What should be implemented next for production

- Replace mock agent logic with real model-backed LangGraph workflows
- Move persistence to Postgres and add durable async execution infrastructure
- Add streaming task updates, better failure recovery, and retry policies
- Introduce richer tool integrations, retrieval, and stronger permission enforcement
- Add auth, multi-user workspaces, and operational monitoring
