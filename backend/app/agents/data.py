from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.agents.configs.data import DATA_AGENT_CONFIG
from app.agents.contracts import DataOutput
from app.permissions.roles import Permission, assert_permission
from app.tools.base import ToolInvocationContext


class DataAgent(BaseAgent):
    name = DATA_AGENT_CONFIG.name
    prompt = DATA_AGENT_CONFIG.prompt
    capability_summary = DATA_AGENT_CONFIG.capability_summary

    def run(self, context: AgentContext):
        assert_permission(self.name, Permission.READ_CSV)
        if not context.task.uploaded_file_name or not context.task.uploaded_file_name.endswith(".csv"):
            raise ValueError("A CSV file is required for data analysis tasks.")

        structured = self.tool_registry.csv_profiler.invoke(ToolInvocationContext(agent=self.name, task=context.task))
        model_output = self.try_structured_completion(
            user_prompt=(
                f"Task: {context.task.prompt}\n"
                f"CSV summary: {structured.model_dump()}\n"
                "Return a concise analytical summary with observations and next steps."
            ),
            response_model=DataOutput,
        )
        if model_output:
            return self.result(
                "Profiled the uploaded dataset and enriched the analysis with the configured model provider.",
                model_output,
                "Send to critic for gap analysis and suggested follow-up.",
            )

        summary = (
            f"Profiled {structured.row_count} rows across {structured.column_count} columns and generated "
            "basic data-quality notes."
        )
        return self.result(summary, structured, "Send to critic for gap analysis and suggested follow-up.")
