from app.services.llm_service import ask_llm


async def recommendation_node(state: dict):
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

    response = ask_llm(prompt)

    state["recommendation"] = response

    return state