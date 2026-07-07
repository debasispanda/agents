
import os
from dotenv import load_dotenv
import requests
from rich import json

load_dotenv(override=True)

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")

pushover_url = "https://api.pushover.net/1/messages.json"


def push(text):
    requests.post(
        pushover_url,
        data={
            "token": pushover_token,
            "user": pushover_user,
            "message": text,
        },
    )

def record_user_details(email, name, notes):
    details = f"Recording interest from {name} with email {email}."
    details += f"{notes}." if notes else "."
    push(details)
    return "OK"

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided a name and an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of the user"},
            "name": {"type": "string", "description": "The name of the user"},
            "notes": {"type": "string", "description": "Any additional info about the conversation that's worth recording to give context"}
        },
        "required": ["email", "name"],
        "additionalProperties": False
    }
}

def record_unknown_question(question):
    push(f"Received a question outside of my expertise. Q: {question}")
    return "OK"

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool when there is a question outside the context.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": { "type": "string", "description": "Question from the user."}
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json}, {"type": "function", "function": record_unknown_question_json}]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question
}

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        globals().get(tool_name)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else f"Unknown tool: {tool_name}"
        print(f"Tool called: {tool_name}", flush=True)
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
