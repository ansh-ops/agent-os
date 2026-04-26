from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from app.agents.base import AgentContext
from app.agents.critic import CriticAgent
from app.agents.data import DataAgent
from app.agents.planning import PlanningAgent
from app.agents.research import ResearchAgent
from app.memory.store import SharedMemoryStore
from app.models.provider import get_model_provider
from app.orchestration.graph import get_graph_runner
from app.permissions.roles import Permission, assert_permission
from app.schemas.task import (
    AgentName,
    AgentResult,
    ArtifactType,
    MemoryEntryType,
    TaskArtifact,
    TaskRecord,
    TaskStatus,
    TaskType,
    TraceEntry,
    TraceStatus,
)
from app.tools.registry import ToolRegistry


class Supervisor:
    def __init__(self, memory_store: SharedMemoryStore) -> None:
        self.memory_store = memory_store
        model_provider = get_model_provider()
        tool_registry = ToolRegistry()
        self.graph = get_graph_runner()
        self.research_agent = ResearchAgent(model_provider=model_provider, tool_registry=tool_registry)
        self.data_agent = DataAgent(model_provider=model_provider, tool_registry=tool_registry)
        self.planning_agent = PlanningAgent(model_provider=model_provider, tool_registry=tool_registry)
        self.critic_agent = CriticAgent(model_provider=model_provider, tool_registry=tool_registry)

    def infer_task_type(self, task: TaskRecord) -> TaskType:
        if task.task_type != TaskType.AUTO:
            return task.task_type

        prompt = task.prompt.lower()
        if task.uploaded_file_name and task.uploaded_file_name.endswith(".csv"):
            return TaskType.DATA
        if any(keyword in prompt for keyword in ("plan", "roadmap", "milestone", "project")):
            return TaskType.PLANNING
        if any(keyword in prompt for keyword in ("csv", "dataset", "table", "analyze data")):
            return TaskType.DATA
        return TaskType.RESEARCH

    def choose_agents(self, task_type: TaskType) -> list[AgentName]:
        route_map = {
            TaskType.RESEARCH: [AgentName.RESEARCH, AgentName.CRITIC],
            TaskType.PLANNING: [AgentName.PLANNING, AgentName.CRITIC],
            TaskType.DATA: [AgentName.DATA, AgentName.CRITIC],
        }
        return route_map[task_type]

    def run(self, task: TaskRecord) -> TaskRecord:
        assert_permission(AgentName.SUPERVISOR, Permission.COORDINATE_WORKFLOW)
        inferred_type = self.infer_task_type(task)
        task.inferred_task_type = inferred_type
        task.status = TaskStatus.PLANNING
        self.memory_store.add_entry(
            task,
            entry_type=MemoryEntryType.TASK_SUMMARY,
            title="Task Summary",
            content=task.prompt,
            source_agent=AgentName.SUPERVISOR,
        )
        if task.uploaded_file_text:
            self.memory_store.add_entry(
                task,
                entry_type=MemoryEntryType.EXTRACTED_FACT,
                title="Uploaded Document",
                content=(
                    f"{task.uploaded_file_name} ingested as {task.uploaded_file_type}. "
                    f"Extracted {len(task.uploaded_file_text)} characters for agent context."
                ),
                source_agent=AgentName.SUPERVISOR,
            )
        elif task.uploaded_file_error:
            self.memory_store.add_entry(
                task,
                entry_type=MemoryEntryType.EXECUTION_EVENT,
                title="Document Ingestion Warning",
                content=task.uploaded_file_error,
                source_agent=AgentName.SUPERVISOR,
            )

        routes = self.choose_agents(inferred_type)
        self.graph.invoke(
            {
                "task_type": inferred_type.value,
                "next_agent": routes[0].value if routes else "",
                "critic_required": AgentName.CRITIC in routes,
            }
        )
        for agent_name in routes:
            task.status = TaskStatus.WAITING_ON_AGENT if agent_name != AgentName.CRITIC else TaskStatus.UNDER_REVIEW
            context = AgentContext(
                task=task,
                shared_facts=self._shared_facts(task.memory),
                prior_outputs=task.agent_outputs,
            )
            trace = TraceEntry(
                agent=agent_name,
                step_name=f"{agent_name.value}_run",
                prompt_summary=task.prompt,
                status=TraceStatus.STARTED,
            )
            task.traces.append(trace)
            try:
                result = self._run_agent(agent_name, context)
                trace.status = TraceStatus.COMPLETED
                trace.finished_at = datetime.now(timezone.utc)
                trace.output_summary = result.summary
            except Exception as exc:
                trace.status = TraceStatus.FAILED
                trace.finished_at = datetime.now(timezone.utc)
                trace.error = str(exc)
                raise
            task.agent_outputs.append(result)
            self.memory_store.add_entry(
                task,
                entry_type=MemoryEntryType.AGENT_OUTPUT,
                title=f"{agent_name.value} output",
                content=result.summary,
                source_agent=agent_name,
                metadata={"next_action": result.suggested_next_action or ""},
            )
            self._store_extracted_facts(task, agent_name, result)

        task.status = TaskStatus.COMPLETED
        task.result_sections = self._build_result_sections(task)
        task.result = self._render_markdown_result(task)
        task.artifacts = [
            TaskArtifact(name="final-report.md", artifact_type=ArtifactType.TEXT, content=task.result),
            TaskArtifact(
                name="final-report.json",
                artifact_type=ArtifactType.JSON,
                content=task.model_dump_json(indent=2),
            ),
        ]
        self.memory_store.add_entry(
            task,
            entry_type=MemoryEntryType.FINAL_ARTIFACT,
            title="Final Report",
            content="Final report and JSON export are ready for download.",
            source_agent=AgentName.SUPERVISOR,
        )
        return task

    def _run_agent(self, agent_name: AgentName, context: AgentContext) -> AgentResult:
        agents = {
            AgentName.RESEARCH: self.research_agent,
            AgentName.DATA: self.data_agent,
            AgentName.PLANNING: self.planning_agent,
            AgentName.CRITIC: self.critic_agent,
        }
        return agents[agent_name].run(context)

    def _shared_facts(self, memory_entries: Iterable) -> list[str]:
        return [entry.content for entry in memory_entries if entry.type == MemoryEntryType.EXTRACTED_FACT]

    def _store_extracted_facts(self, task: TaskRecord, agent_name: AgentName, result: AgentResult) -> None:
        output = result.structured_output
        candidates: list[str] = []
        if isinstance(output.get("findings"), list):
            candidates.extend(str(item) for item in output["findings"][:3])
        if isinstance(output.get("observations"), list):
            candidates.extend(str(item) for item in output["observations"][:3])
        if isinstance(output.get("next_steps"), list):
            candidates.extend(f"Next: {item}" for item in output["next_steps"][:2])

        for fact in candidates[:4]:
            self.memory_store.add_entry(
                task,
                entry_type=MemoryEntryType.EXTRACTED_FACT,
                title=f"{agent_name.value} fact",
                content=fact,
                source_agent=agent_name,
            )

    def _build_result_sections(self, task: TaskRecord) -> list[dict[str, object]]:
        sections = [
            {
                "title": "Task Overview",
                "content": task.prompt,
            }
        ]
        for output in task.agent_outputs:
            sections.append(
                {
                    "title": output.agent.value.replace("_", " ").title(),
                    "content": output.summary,
                    "details": output.structured_output,
                }
            )
        return sections

    def _render_markdown_result(self, task: TaskRecord) -> str:
        lines = [
            "# Agent OS Final Output",
            "",
            f"Task: {task.prompt}",
            f"Inferred task type: {task.inferred_task_type.value if task.inferred_task_type else task.task_type.value}",
            "",
            "## Execution Summary",
        ]
        for output in task.agent_outputs:
            lines.extend(
                [
                    f"### {output.agent.value.replace('_', ' ').title()}",
                    output.summary,
                    "",
                ]
            )
        critic_output = next((item for item in task.agent_outputs if item.agent == AgentName.CRITIC), None)
        if critic_output:
            lines.extend(
                [
                    "## Review Recommendation",
                    critic_output.structured_output.get("recommendation", "Approve final response."),
                    "",
                ]
            )
        return "\n".join(lines)
