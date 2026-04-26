from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.agents.configs.critic import CRITIC_AGENT_CONFIG
from app.agents.contracts import CriticOutput
from app.permissions.roles import Permission, assert_permission


class CriticAgent(BaseAgent):
    name = CRITIC_AGENT_CONFIG.name
    prompt = CRITIC_AGENT_CONFIG.prompt
    capability_summary = CRITIC_AGENT_CONFIG.capability_summary

    def run(self, context: AgentContext):
        assert_permission(self.name, Permission.READ_AGENT_OUTPUTS)
        assert_permission(self.name, Permission.REVIEW_OUTPUTS)
        if not context.prior_outputs:
            raise ValueError("Critic agent requires prior outputs to review.")

        primary_output = context.prior_outputs[-1]
        model_output = self.try_structured_completion(
            user_prompt=(
                f"Reviewed agent: {primary_output.agent.value}\n"
                f"Summary: {primary_output.summary}\n"
                f"Structured output: {primary_output.structured_output}\n"
                "Return issues, recommendation, and quality score."
            ),
            response_model=CriticOutput,
        )
        if model_output:
            return self.result(
                "Reviewed the specialist output using the configured model provider.",
                model_output,
                model_output.recommendation,
            )

        issues = []
        next_action = "Approve final response."

        if len(primary_output.summary) < 40:
            issues.append("The specialist summary is brief and may benefit from more supporting detail.")
            next_action = "Consider rerunning the specialist agent with richer context."

        if not primary_output.structured_output:
            issues.append("Structured output is empty, which weakens downstream extensibility.")
            next_action = "Regenerate structured output before completion."

        if not issues:
            issues.append("Output is coherent for an MVP workflow and ready to present.")

        summary = "Reviewed the specialist output for completeness, support, and execution readiness."
        structured = CriticOutput(
            reviewed_agent=primary_output.agent.value,
            issues=issues,
            recommendation=next_action,
            quality_score=0.86 if len(issues) == 1 and "ready to present" in issues[0] else 0.62,
        )
        return self.result(summary, structured, next_action)
