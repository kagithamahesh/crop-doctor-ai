import json
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url=settings.GROQ_BASE_URL,
)

async def ask_llm(prompt: str) -> dict:
    response = await client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
    {
    "role": "system",
    "content": (
    "You are a senior agricultural agronomist. "
    "Always return valid JSON only."
    ),
    },
    {
    "role": "user",
    "content": prompt,
    },
    ],
    temperature=0.2,
    response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON from LLM",
            "raw_response": content,
        }