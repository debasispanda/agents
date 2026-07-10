import os
import sys
from pathlib import Path

from agents import Agent, function_tool

from contexts import instruction1, instruction2, instruction3, pick_instruction, send_instruction

parent_dir = Path(__file__).resolve().parent.parent
# Add the parent directory to the module search path
sys.path.append(str(parent_dir))

from common.tools.messenger import send_message

MODEL_NAME = "gpt-5.4-mini"

sales_agent1 = Agent(name="Professional Sales Agent", instructions=instruction1, model=MODEL_NAME)
sales_agent2 = Agent(name="Humorous Sales Agent", instructions=instruction2, model=MODEL_NAME)
sales_agent3 = Agent(name="Executive Sales Agent", instructions=instruction3, model=MODEL_NAME)

email_picker_agent = Agent(name="Sales Email Picker", instructions=pick_instruction, model=MODEL_NAME)

@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str):
    """
    Use this tool to send emails using given subject and body to all sales prospects.

    Args:
        subject: The subject of the email
        text_body: The body of the email in plain text format
        html_body: The HTML body of the email
    """
    send_message(subject, text_body, html_body)
    return "Email sent successfully!"

email_sender = Agent(name="Sale Email Sender", instructions=send_instruction, model=MODEL_NAME, tools=[send_email_tool])
