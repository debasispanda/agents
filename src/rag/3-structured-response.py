from pydantic_ai import Agent
import nest_asyncio

from models.output import SearchAnswer

from utils.tools import grep, list_files, read_file

nest_asyncio.apply()

agent = Agent(
    model="openai:gpt-5.5",
    tools=[list_files, grep, read_file],
    output_type=SearchAnswer,
    instructions=(
        "Search notes with list_files, grep, read_file. Cite files.",
        "If evidence is missing, say no."
    )
)

if __name__ == "__main__":
    question = "Why does our nightly deploy job run at 03:47 UTC specifically?"
    result = agent.run_sync(question)

    answer = result.output

    print(f"\nAnswer: {answer.answer}")
    print("\nCitations:")
    for c in answer.citations:
        print(f" - {c.file}:{c.line_number}")
        print(f"     {c.quote}")
