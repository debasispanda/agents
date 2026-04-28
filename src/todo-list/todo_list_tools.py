import json
from openai import OpenAI
from dotenv import load_dotenv
from todo_list import show, create_todos, mark_complete

load_dotenv()
openai = OpenAI()

create_todos_json = {
    "name": "create_todos",
    "description": "Create new todos with the given descriptions and return the full updated todo list.",
    "parameters": {
        "type": "object",
        "properties": {
            "descriptions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "A list of todo descriptions to be added."
            },
        },
        "required": ["descriptions"],
        "additionalProperties": False
    }
}

mark_complete_json = {
    "name": "mark_complete",
    "description": "Mark a specific todo as complete or incomplete based on the provided index and return the full updated todo list.",
    "parameters": {
        "type": "object",
        "properties": {
            "index": {
                "type": "integer",
                "title": "Todo Index",
                "description": "The 1-based index of the todo to be marked."
            },
            "completion_notes": {
                "type": "string",
                "title": "Completion Notes",
                "description": "Notes about how you completed the todo in rich console markup."
            },
        },
        "required": ["index", "completion_notes"],
        "additionalProperties": False
    }
}

# Tools list to be used by the agent
tools = [{ "type": "function", "function": create_todos_json }, { "type": "function", "function": mark_complete_json  }]

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)
        tool = globals().get(tool_name)
        
        result = tool(**tool_args) if tool else {}
        results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
    return results

def loop(messages):
    done = False
    while not done:
        response = openai.chat.completions.create(
            model="gpt-5.2",
            messages=messages,
            tools=tools,
            reasoning_effort="none",
        )

        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    show(response.choices[0].message.content)


system_message = """
You are given a problem to solve, by using your todo tools to plan a list of steps, then carrying out each step in turn.
Now use the todo list tools, create a plan, carry out the steps, and reply with the solution.
If any quantity isn't provided in the question, then include a step to come up with a reasonable estimate.
Provide your solution in Rich console markup without code blocks.
Do not ask the user questions or clarification; respond only with the answer after using your tools.
"""
user_message = """"
A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?
"""
messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]

todos, completed = [], []
loop(messages)