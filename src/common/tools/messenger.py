import os
import requests
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv(override=True)

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = os.getenv("PUSHOVER_URL")

_EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
_EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
_EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

USE_EMAIL = _EMAIL_SMTP_SERVER and _EMAIL_ADDRESS and _EMAIL_APP_PASSWORD

def send_email(subject: str, text_body: str, html_body: str):
    message = EmailMessage()
    message["From"] = _EMAIL_ADDRESS
    message["To"] = _EMAIL_ADDRESS
    message["Subject"] = subject
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(_EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(_EMAIL_ADDRESS, _EMAIL_APP_PASSWORD)
        server.send_message(message)

def send_notification(message: str):
    print("Sending notification.")
    payload = { "user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message }
    requests.post(PUSHOVER_URL, data=payload)

def send_message(subject: str, text_body: str, html_body: str):
    if (USE_EMAIL):
        return send_email(subject, text_body, html_body)
    send_notification(f"Subject: {subject}\n\n{text_body}")
