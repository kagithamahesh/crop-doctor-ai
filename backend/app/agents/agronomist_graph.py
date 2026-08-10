from langgraph.graph import StateGraph, END

from app.agents.state import DiagnosisState
from app.agents.weather_node import weather_node
from app.agents.market_node import market_node
from app.agents.knowledge_node import knowledge_node
from app.agents.recommendation_node import recommendation_node

graph = StateGraph(DiagnosisState)

graph.add_node("weather", weather_node)
graph.add_node("market", market_node)
graph.add_node("knowledge", knowledge_node)
graph.add_node("recommendation", recommendation_node)

graph.set_entry_point("weather")

graph.add_edge("weather", "market")
graph.add_edge("market", "knowledge")
graph.add_edge("knowledge", "recommendation")
graph.add_edge("recommendation", END)

agronomist_agent = graph.compile()