
import os
from dotenv import load_dotenv
import requests
from agents import function_tool

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

@function_tool
def record_user_details(email: str, name: str, notes: str | None) -> str:
    """
    Use this tool to record that a user is interested in being in touch and provided a name and an email address.
    """
    details = f"Recording interest from {name} with email {email}."
    details += f"{notes}." if notes else "."
    push(details)
    return "OK"

@function_tool
def record_unknown_question(question: str) -> str:
    """Always use this tool when there is a question outside the context."""
    push(f"Received a question outside of my expertise. Q: {question}")
    return "OK"

tools = [record_user_details, record_unknown_question]