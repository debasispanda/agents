import asyncio
from agents import trace, Runner
from contexts import task
from tools import sales_manager

async def start():
    with trace("Sales Manager across different models"):
        result = await Runner.run(sales_manager, task)

    print(f"Final Response: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(start())
