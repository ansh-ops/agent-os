from __future__ import annotations

from app.agents.base import AgentContext, BaseAgent
from app.agents.configs.planning import PLANNING_AGENT_CONFIG
from app.agents.contracts import PlanningOutput, PlanningPhase, PlanningTaskItem
from app.permissions.roles import Permission, assert_permission


class PlanningAgent(BaseAgent):
    name = PLANNING_AGENT_CONFIG.name
    prompt = PLANNING_AGENT_CONFIG.prompt
    capability_summary = PLANNING_AGENT_CONFIG.capability_summary

    def run(self, context: AgentContext):
        assert_permission(self.name, Permission.READ_CONTEXT)
        assert_permission(self.name, Permission.READ_AGENT_OUTPUTS)
        goal = context.task.prompt
        context_summary = context.task.context_text or "No additional planning context provided."
        model_output = self.try_structured_completion(
            user_prompt=(
                f"Goal: {goal}\n"
                f"Context: {context_summary}\n"
                "Return phases, task tree items, risks, and practical next steps."
            ),
            response_model=PlanningOutput,
        )
        if model_output:
            return self.result(
                "Converted the request into a structured implementation plan with the configured model provider.",
                model_output,
                "Send to critic for consistency and completeness checks.",
            )

        tasks = [
            PlanningTaskItem(title="Clarify scope and success criteria", owner="human", status="todo"),
            PlanningTaskItem(title="Gather required inputs and constraints", owner="agent", status="todo"),
            PlanningTaskItem(title="Draft implementation plan", owner="planning_agent", status="todo"),
            PlanningTaskItem(title="Review risks and dependencies", owner="critic_agent", status="todo"),
            PlanningTaskItem(title="Execute highest-priority workstream", owner="human", status="todo"),
        ]
        summary = "Converted the request into a phased project plan with execution-ready tasks."
        structured = PlanningOutput(
            goal=goal,
            phases=[
                PlanningPhase(
                    name="Discovery",
                    deliverables=["Scope statement", "Inputs inventory", f"Context alignment: {context_summary[:80]}"],
                ),
                PlanningPhase(name="Execution", deliverables=["Task checklist", "Implementation sequence", "Risk review"]),
            ],
            task_tree=tasks,
            risks=[
                "Missing requirements can create rework.",
                "Dependencies may block execution if they are not identified early.",
            ],
            next_steps=[task.title for task in tasks[:3]],
        )
        return self.result(summary, structured, "Send to critic for consistency and completeness checks.")
