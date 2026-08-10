from app.services.llm_service import ask_llm

from app.agents.state import DiagnosisState


async def recommendation_node(state: DiagnosisState) -> DiagnosisState:
    prompt = f"""
You are an expert agricultural agronomist.

Crop: {state['crop']}
Disease: {state['disease']}

Weather:
{state['weather']}

Market:
{state['market']}

Knowledge Base:
{state['knowledge']}

Provide:

1. Disease explanation
2. Immediate treatment
3. Pesticide recommendation
4. Irrigation advice
5. Estimated risk
6. Best selling strategy
7. Follow-up action
"""

    response = await ask_llm(prompt)

    state["recommendation"] = response

    return state