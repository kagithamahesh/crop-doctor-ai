import asyncio

from app.services.llm_service import generate_recommendation
from app.agents.state import DiagnosisState


async def recommendation_node(state: DiagnosisState) -> DiagnosisState:
    knowledge = state.get("knowledge", [])

    knowledge_text = "\n\n".join(
        [
            f"Title: {doc['title']}\nSource: {doc['source']}\nContent: {doc['content']}"
            for doc in knowledge
        ]
    )

    prompt = f"""
Crop: {state['crop']}
Disease: {state['disease']}
Confidence: {state['confidence']}

Weather:
{state['weather']}

Market:
{state['market']}

Retrieved agricultural knowledge:
{knowledge_text}

Generate a detailed recommendation as a JSON object with these keys:

1. "disease_explanation"
2. "immediate_treatment"
3. "fungicide_or_pesticide"
4. "irrigation_advice"
5. "spraying_recommendation"
6. "market_strategy"
7. "risk_assessment"
8. "follow_up_monitoring"
9. "sources"

Keep all values practical and evidence-based. Return only valid JSON.
"""

    recommendation = await asyncio.get_event_loop().run_in_executor(
        None, generate_recommendation, prompt
    )

    state["recommendation"] = recommendation

    return state