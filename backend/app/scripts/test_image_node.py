import asyncio

from app.agents.diagnosis_graph import build_graph


async def main():
    graph = build_graph()

    state = {
        "image_path": "uploads/f56a727d-20da-41fe-9bc2-2c6455399cde.jpeg",
        "location": "Hyderabad",
    }

    result = await graph.ainvoke(state)

    print("Final graph output:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())