from agents import Agent, Runner

import gradio as gr

from tools import tools
from context import TWIN_SYSTEM_PROMPT

MODEL_NAME = "gpt-5.4-mini"


async def chat(message, history):
    agent = Agent(name="Digital Twin", instructions=f"{TWIN_SYSTEM_PROMPT} {history}", model=MODEL_NAME, tools=tools)
    result = await Runner.run(agent, input=message)
    return result.final_output

def start_chat():
    gr.ChatInterface(chat).launch()

if __name__ == "__main__":
    start_chat()
