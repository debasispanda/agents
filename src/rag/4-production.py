import logging
import nest_asyncio
import time
from models.output import SearchAnswer
from pydantic_ai import Agent, UsageLimits
from utils.production_tools import list_files, grep, read_file
from configs.constants import AGENT_REQUEST_LIMIT

nest_asyncio.apply()

logger = logging.getLogger(__name__)

agent = Agent(
    # model="openai:gpt-5.5",
    model="openai:gpt-4.1-nano",  # faster
    tools=[list_files, grep, read_file],
    output_type=SearchAnswer,
    instructions=(
        "Search notes with list_files, grep, read_file. Cite files.",
        "Adapt to Error/No matches"
    )
)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    start = time.perf_counter()
    result = agent.run_sync(
        "Why does our nightly deploy job run at 03:47 UTC specifically?",
        usage_limits=UsageLimits(request_limit=AGENT_REQUEST_LIMIT),
    )
    elapsed = time.perf_counter() - start

    print("\nAgent:", result.output.answer)
    print("\nCitations:")
    for citation in result.output.citations:
        print(f"  - {citation.file}")
        for line in citation.quote.splitlines():
            print(f"      {line}")

    usage = result.usage
    print(
        f"\nUsage: {usage.requests} requests, {usage.tool_calls} tool calls, "
        f"{usage.input_tokens} input + {usage.output_tokens} output tokens, "
        f"{elapsed:.1f}s"
    )
