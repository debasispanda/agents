from pydantic_ai import Agent
from pydantic_ai.messages import FunctionToolCallEvent, FunctionToolResultEvent
import asyncio
import nest_asyncio
from utils.tools import list_files, grep, read_file
from utils.stream import format_tool_results

nest_asyncio.apply()

agent = Agent(
    model="openai:gpt-5.5",
    tools=[list_files, grep, read_file],
    instructions=(
        "Search notes with list_files, grep and read_file. Cite file.",
        "If evidence is missing, say no."
    )
)

async def async_run_with_visible_steps(question: str, debug: bool = False) -> str:
    print(f"Q: {question}\n")
    print("")
    tool_names: dict[str, str] = {}
    async with agent.iter(question) as run:
        async for node in run:
            if Agent.is_call_tools_node(node):
                async with node.stream(run.ctx) as tool_stream:
                    async for event in tool_stream:
                        if isinstance(event, FunctionToolCallEvent):
                            tool_names[event.tool_call_id] = event.part.tool_name
                            print(
                                f"-> {event.part.tool_name} {event.part.args_as_json_str()}"
                            )
                        elif debug and isinstance(event, FunctionToolResultEvent):
                            print(format_tool_results(event, tool_names))
    print("---done---")
    return run.result.output


if __name__ == "__main__":
    question = "Why does our nightly deploy job run at 03:47 UTC specifically?"

    answer = asyncio.run(async_run_with_visible_steps(question))
    print(f"A: {answer}")
