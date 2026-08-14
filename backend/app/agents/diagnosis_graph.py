from langgraph.graph import StateGraph, END

from app.agents.state import DiagnosisState
from app.agents.image_analysis_node import image_analysis_node
from app.agents.parallel_data_node import parallel_data_node
from app.agents.recommendation_node import recommendation_node


def build_graph():
    graph = StateGraph(DiagnosisState)

    graph.add_node(
        "image_analysis",
        image_analysis_node,
    )

    graph.add_node(
        "parallel_data",
        parallel_data_node,
    )

    graph.add_node(
        "recommendation",
        recommendation_node,
    )

    graph.set_entry_point("image_analysis")

    graph.add_edge(
        "image_analysis",
        "parallel_data",
    )

    graph.add_edge(
        "parallel_data",
        "recommendation",
    )

    graph.add_edge(
        "recommendation",
        END,
    )

    return graph.compile()