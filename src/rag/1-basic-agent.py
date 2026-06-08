from pydantic_ai import Agent
import nest_asyncio
from utils.tools import list_files, grep, read_file

nest_asyncio.apply()

agent = Agent(
    model="openai:gpt-5.5",
    tools=[list_files, grep, read_file],
    instructions=(
        "Search notes with list_files, grep and read_file. Cite file.",
        "If evidence is missing, say no."
    )
)

if __name__ == "__main__":
    question = "Why does our nightly deploy job run at 03:47 UTC specifically?"

    result = agent.run_sync(question)

    print(f"\nQ: {question}")
    print(f"\nA: {result.output}")
    print(f"\nUsage: {result.usage()}")
