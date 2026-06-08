from pydantic_ai.messages import FunctionToolResultEvent

def preview(content: any) -> str:
    if isinstance(content, list):
        lines = "\n    ".join(str(item) for item in content)
        return f"{len(lines)} results.\n {lines}" if content else "0 results"
    return str(content).splitlines()[0][:120]

def format_tool_results(event: FunctionToolResultEvent, tool_names: dict[str, str]) -> str:
    tool_name = tool_names.get(event.tool_call_id, event.part.tool_name)
    return f" <- {tool_name}: {preview(event.part.content)}"
