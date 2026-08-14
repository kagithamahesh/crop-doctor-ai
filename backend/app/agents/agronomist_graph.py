from langgraph.graph import StateGraph, END

from app.agents.state import DiagnosisState
from app.agents.image_analysis_node import image_analysis_node
from app.agents.supervisor_node import supervisor_node
from app.agents.parallel_data_node import parallel_data_node
from app.agents.recommendation_node import recommendation_node
from app.agents.human_review_node import human_review_node


def build_graph():
    graph = StateGraph(DiagnosisState)

    graph.add_node("image_analysis", image_analysis_node)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("parallel_data", parallel_data_node)
    graph.add_node("recommendation", recommendation_node)
    graph.add_node("human_review", human_review_node)

    graph.set_entry_point("image_analysis")

    graph.add_edge("image_analysis", "supervisor")

    def route_decision(state: DiagnosisState):
        return state.get("route", "human_review")

    graph.add_conditional_edges(
        "supervisor",
        route_decision,
        {
            "parallel_data": "parallel_data",
            "human_review": "human_review",
        },
    )

    graph.add_edge("parallel_data", "recommendation")
    graph.add_edge("recommendation", END)
    graph.add_edge("human_review", END)

    return graph.compile()


agronomist_agent = build_graph()