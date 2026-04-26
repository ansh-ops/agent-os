from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.agents.configs.research import RESEARCH_AGENT_CONFIG
from app.agents.contracts import ResearchOutput
from app.permissions.roles import Permission, assert_permission
from app.tools.base import ToolInvocationContext


class ResearchAgent(BaseAgent):
    name = RESEARCH_AGENT_CONFIG.name
    prompt = RESEARCH_AGENT_CONFIG.prompt
    capability_summary = RESEARCH_AGENT_CONFIG.capability_summary

    def run(self, context: AgentContext):
        assert_permission(self.name, Permission.READ_CONTEXT)
        tool_result = self.tool_registry.context_reader.invoke(ToolInvocationContext(agent=self.name, task=context.task))
        raw_context = " ".join(
            part for part in [tool_result.get("context_text", ""), tool_result.get("uploaded_text", "")] if part
        ) or "No additional supporting context was provided."
        source_note = (
            f" Uploaded source: {tool_result.get('uploaded_file_name')}."
            if tool_result.get("uploaded_file_name") and tool_result.get("uploaded_text")
            else ""
        )
        model_output = self.try_structured_completion(
            user_prompt=(
                f"Task: {context.task.prompt}\n"
                f"Context: {raw_context}\n"
                "Return key findings, a recommended summary, and clear caveats."
            ),
            response_model=ResearchOutput,
        )
        if model_output:
            return self.result(
                "Researched the task using the configured model provider and structured internal context.",
                model_output,
                "Send to critic for quality review.",
            )

        bullets = [
            sentence.strip()
            for sentence in raw_context.replace("\n", " ").split(".")
            if sentence.strip()
        ][:5]
        findings = bullets or ["The request should be answered using the prompt itself as the primary source."]
        summary = f"Researched the task using provided context and extracted {len(findings)} key findings.{source_note}"
        structured = ResearchOutput(
            task_goal=context.task.prompt,
            findings=findings,
            recommended_summary=" ".join(findings[:3]),
            caveats=[
                "This MVP uses local context and heuristics by default.",
                "External web retrieval can be added as a separate permissioned tool.",
            ],
        )
        return self.result(summary, structured, "Send to critic for quality review.")
