from __future__ import annotations

from typing import Any, TypedDict


class GraphState(TypedDict, total=False):
    task_type: str
    next_agent: str
    critic_required: bool


class FallbackGraphRunner:
    def invoke(self, state: GraphState) -> GraphState:
        return state


def get_graph_runner() -> Any:
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError:
        return FallbackGraphRunner()

    graph = StateGraph(GraphState)
    graph.add_node("supervisor", lambda state: state)
    graph.add_node("specialist", lambda state: state)
    graph.add_node("critic", lambda state: state)
    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        lambda state: "specialist" if state.get("critic_required", True) else END,
        {"specialist": "specialist", END: END},
    )
    graph.add_edge("specialist", "critic")
    graph.add_edge("critic", END)
    return graph.compile()
