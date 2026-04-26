# Agent OS Crash Course

## 1. What this project is

Agent OS is a full-stack MVP for a multi-agent AI workflow platform.

Instead of treating AI like one chatbot, this project treats AI like a small team:

- a `supervisor` receives the task
- a specialist agent does the core work
- a `critic` reviews the output
- the system stores memory, permissions, workflow state, and traces
- the UI shows what happened step by step

The goal is to make AI workflows visible, structured, and extensible.

## 2. High-level architecture

The project has two major parts:

### Backend

The backend is built with FastAPI and handles:

- task creation
- file upload handling
- orchestration
- agent execution
- shared memory
- permissions
- workflow state
- provider status checks
- final artifact generation

Main backend folders:

- `backend/app/api`: HTTP routes
- `backend/app/agents`: agent implementations
- `backend/app/orchestration`: supervisor and graph flow
- `backend/app/memory`: shared memory handling
- `backend/app/permissions`: agent permission rules
- `backend/app/state`: task persistence
- `backend/app/services`: task execution and system status
- `backend/app/models`: LLM provider abstraction
- `backend/app/tools`: permission-aware tool layer
- `backend/app/schemas`: typed request/response models

### Frontend

The frontend is built with Next.js, TypeScript, and Tailwind.

It gives us a dashboard with:

- task submission
- recent tasks
- workflow trace
- shared memory view
- final output view
- runtime provider badge

Main frontend folders:

- `frontend/src/app`: page shell
- `frontend/src/components`: dashboard UI pieces
- `frontend/src/lib`: API clients and sample task presets
- `frontend/src/types`: frontend contracts

## 3. How the system works end to end

When a user submits a task, this is the flow:

1. The frontend sends the task to `POST /api/tasks`.
2. FastAPI creates a new `TaskRecord`.
3. The task is stored in a local JSON-backed task store.
4. A background task starts execution.
5. The `supervisor` inspects the task and decides the task type.
6. The supervisor chooses which specialist agent should run.
7. The graph runner initializes the execution path.
8. The specialist agent runs with a restricted tool/permission scope.
9. The agent writes outputs into shared memory and traces.
10. The `critic` reviews the specialist output.
11. The supervisor merges all outputs into final sections and artifacts.
12. The frontend polls the task and renders status, trace, memory, and final output.

## 4. Task types supported

The MVP supports three main flows:

### Research

Example:

`Research multi-agent orchestration patterns and summarize the strongest ideas.`

Flow:

`supervisor -> research_agent -> critic_agent`

### Planning

Example:

`Plan a 2-week roadmap for an internal AI product.`

Flow:

`supervisor -> planning_agent -> critic_agent`

### Data

Example:

`Analyze this CSV and suggest next steps.`

Flow:

`supervisor -> data_agent -> critic_agent`

## 5. How orchestration is implemented

There are two orchestration layers in the project:

### Supervisor layer

Implemented in:

- `backend/app/orchestration/supervisor.py`

The supervisor is responsible for:

- classifying the task
- choosing the route
- creating memory entries
- creating trace entries
- calling the correct agents
- building the final response

### Graph layer

Implemented in:

- `backend/app/orchestration/graph.py`

This is the LangGraph-ready orchestration layer.

Right now it provides:

- a simple graph execution path
- a safe fallback if LangGraph is unavailable
- a clean place to grow into richer agent routing later

This matters because long-term, multi-agent systems usually need:

- branching
- retries
- review loops
- conditional routing
- resumability

LangGraph is a natural fit for that evolution.

## 6. How agents are implemented

Each agent is a class with a clear interface.

Base class:

- `backend/app/agents/base.py`

Each agent receives:

- `AgentContext`

This contains:

- the current task
- shared facts
- prior agent outputs

Each agent returns:

- `AgentResult`

This includes:

- agent name
- summary
- structured output
- suggested next action

### Agent configs

Prompts and high-level role descriptions are isolated in:

- `backend/app/agents/configs/research.py`
- `backend/app/agents/configs/planning.py`
- `backend/app/agents/configs/data.py`
- `backend/app/agents/configs/critic.py`

This keeps the role definition separate from the execution logic.

### Structured outputs

Typed structured outputs live in:

- `backend/app/agents/contracts.py`

Examples:

- `ResearchOutput`
- `PlanningOutput`
- `DataOutput`
- `CriticOutput`

This is important because agents are not passing around raw free-form text only. They pass structured data that the rest of the system can safely use.

## 7. What each agent does

### Research Agent

Implemented in:

- `backend/app/agents/research.py`

Responsibilities:

- read prompt/context
- read extracted text from uploaded PDF, DOCX, Markdown, or text files
- extract findings
- produce a structured summary
- include caveats

It can use the context-reader tool and optionally a model provider.

### Planning Agent

Implemented in:

- `backend/app/agents/planning.py`

Responsibilities:

- turn a goal into phases
- create task trees
- call out risks
- generate next steps

### Data Agent

Implemented in:

- `backend/app/agents/data.py`

Responsibilities:

- inspect uploaded CSVs
- profile rows/columns
- generate observations
- recommend next analysis steps

It uses the CSV profiler tool and can optionally enrich the result with the configured model provider.

### Critic Agent

Implemented in:

- `backend/app/agents/critic.py`

Responsibilities:

- review specialist output
- identify weak spots
- recommend approval or refinement

This gives the workflow a review step instead of blindly trusting the first output.

## 8. Shared memory

Shared memory is implemented in:

- `backend/app/memory/store.py`

The memory system is intentionally simple but explicit.

It stores entries such as:

- task summary
- extracted facts
- agent outputs
- execution events
- final artifacts

Why this matters:

- agents can pass useful information through the workflow
- the UI can show intermediate context
- the architecture has a clear upgrade path to more advanced memory later

## 9. Permissions

Permissions are defined in:

- `backend/app/permissions/roles.py`

Examples:

- `research_agent` can read context
- `data_agent` can read CSV data
- `planning_agent` can read prior outputs
- `critic_agent` can review outputs
- `supervisor` coordinates the workflow

These permissions are enforced before tools are used.

This is important because it makes agent boundaries explicit.

## 10. Tool layer

The tool layer is in:

- `backend/app/tools`

It contains permission-aware tools such as:

- `ContextReaderTool`
- `CSVProfilerTool`

Tools are invoked through:

- `ToolInvocationContext`

This gives us a clean mechanism for future expansion, such as:

- web research tools
- database tools
- retrieval/search tools
- code execution tools

## 10A. Document ingestion

Research document ingestion is implemented in:

- `backend/app/services/document_ingestion.py`

Supported research upload formats:

- PDF
- DOCX
- Markdown
- plain text

How it works:

1. The user uploads a document from the task submission panel.
2. The backend stores the uploaded file.
3. The task service extracts text during task creation.
4. The extracted text is stored on the task record.
5. The supervisor writes an ingestion memory entry.
6. The research agent reads the extracted text through the context-reader tool.

This makes research workflows much more realistic because the agent can summarize uploaded source material instead of relying only on a prompt.

## 11. Model provider layer

The provider abstraction is implemented in:

- `backend/app/models/provider.py`

This is how the app separates workflow logic from model vendor logic.

Right now the system supports:

- `gemini` as the default real provider path
- `openai` as an alternate provider path
- `mock` fallback mode

This lets the app run in two modes:

### Mock mode

- local deterministic logic
- no real API dependency
- useful for demos and testing

### Model-backed mode

- uses the configured LLM provider
- returns structured outputs
- makes the agents feel more realistic

## 12. Runtime validation

Provider validation is implemented in:

- `backend/app/services/system_status.py`
- `GET /api/system/status`

The system checks:

- whether a provider key is present
- whether mock mode is enabled
- whether the provider SDK is installed
- whether the provider is reachable

The frontend displays this in a badge so we can instantly see:

- `Mock Mode`
- `LLM Active`
- `LLM Misconfigured`

## 13. Workflow state and traces

Task state is represented using typed enums such as:

- `queued`
- `planning`
- `running`
- `waiting_on_agent`
- `under_review`
- `completed`
- `failed`

Trace entries record:

- which agent ran
- what step it ran
- start/finish time
- status
- summary or error

This makes the system inspectable instead of black-box.

## 14. Persistence

Persistence is handled by:

- `backend/app/state/store.py`

The current implementation uses a local JSON-backed abstraction.

Why this was chosen:

- simple local setup
- no database dependency for the MVP
- easy to understand
- easy to upgrade later to Postgres

## 15. Frontend dashboard

The dashboard is implemented across:

- `frontend/src/app/page.tsx`
- `frontend/src/components/TaskSubmissionPanel.tsx`
- `frontend/src/components/WorkflowView.tsx`
- `frontend/src/components/MemoryView.tsx`
- `frontend/src/components/FinalOutputView.tsx`
- `frontend/src/components/TaskListSidebar.tsx`
- `frontend/src/components/ProviderStatusBadge.tsx`

What the user can do:

- submit a task
- choose a task type
- upload a `.csv`, `.txt`, `.md`, `.pdf`, or `.docx`
- inspect the workflow
- inspect shared memory
- inspect the final output
- download text or JSON results
- see if the system is in mock mode or live LLM mode

## 16. Sample data and demo readiness

Demo assets live in:

- `demo-data/sample_tasks.json`
- `demo-data/sales_pipeline.csv`
- `demo-data/technical-brief-source.txt`
- `docs/resume-portfolio-copy.md`

The frontend also has task presets in:

- `frontend/src/lib/sampleTasks.ts`

This makes the app demo-ready immediately after setup.

## 17. How to run it

### Local mode

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

### Docker mode

```bash
docker compose up --build
```

## 18. How to enable Gemini

Use a root `.env` like this:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
USE_MOCK_AGENTS=false
```

Then rebuild Docker or restart the backend.

If everything is correct, the provider badge should show:

- `LLM Active`

## 19. What is still mocked

Even after the provider upgrade, this is still an MVP.

What is still intentionally limited:

- no real web-browsing tool inside the app
- no long autonomous self-replanning loop
- no durable queue
- no auth
- no multi-user system
- no advanced retrieval
- no enterprise-grade observability

## 20. What this project proves

This project proves that we can build an AI workflow system with:

- clear orchestration
- agent specialization
- typed contracts
- memory
- permissions
- traces
- a usable product UI
- a clean path from mock mode to live provider mode

That makes it a good portfolio project because it demonstrates:

- product thinking
- backend architecture
- full-stack implementation
- AI systems design
- practical MVP scoping

## 21. How to present it on a resume or portfolio

Ready-to-use copy lives in:

- `docs/resume-portfolio-copy.md`

That file includes:

- resume bullets
- portfolio project description
- short pitch
- technical stack
- demo script
- honest limitations
- strong next steps
