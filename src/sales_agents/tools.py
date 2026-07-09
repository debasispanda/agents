import os
import smtplib
import requests
from dotenv import load_dotenv
from email.message import EmailMessage
from agents import Agent, function_tool

from contexts import instruction1, instruction2, instruction3, pick_instruction, send_instruction

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = os.getenv("PUSHOVER_URL")

USE_EMAIL = EMAIL_SMTP_SERVER and EMAIL_ADDRESS and EMAIL_APP_PASSWORD

def send_message(subject: str, text_body: str, html_body: str):
    if (USE_EMAIL):
        return send_email(subject, text_body, html_body)
    send_notification(f"Subject: {subject}\n\n{text_body}")

def send_email(subject: str, text_body: str, html_body: str):
    message = EmailMessage()
    message["From"] = EMAIL_ADDRESS
    message["To"] = EMAIL_ADDRESS
    message["Subject"] = subject
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(message)

def send_notification(message: str):
    print("Sending notification.")
    payload = { "user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message }
    requests.post(PUSHOVER_URL, data=payload)


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
