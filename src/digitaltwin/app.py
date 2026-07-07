from dotenv import load_dotenv
from openai import OpenAI

import gradio as gr

from tools import tools, handle_tool_calls
from context import TWIN_SYSTEM_PROMPT

MODEL_NAME = "gpt-5.4-mini"
openai = OpenAI()

def chat(message, history):
    messages = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
         
    while response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            results = handle_tool_calls(message.tool_calls)
            messages.append(message)
            messages.extend(results)
            response = openai.chat.completions.create(model=MODEL_NAME, messages=messages, tools=tools)
            
    return response.choices[0].message.content

def start_chat():
    gr.ChatInterface(chat).launch()

if __name__ == "__main__":
    start_chat()