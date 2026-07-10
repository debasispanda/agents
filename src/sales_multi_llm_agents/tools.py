import os
import sys
from pathlib import Path
from pydantic import BaseModel, Field

from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, function_tool

from contexts import agent_instruction, manager_instruction

parent_dir = Path(__file__).resolve().parent.parent
# Add the parent directory to the module search path
sys.path.append(str(parent_dir))

from common.tools.messenger import send_message

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=GOOGLE_API_KEY)
openrouter_client = AsyncOpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)

gemini_model = OpenAIChatCompletionsModel(model="gemini-3.1-flash-lite", openai_client=gemini_client)
llama_model = OpenAIChatCompletionsModel(model="meta-llama/llama-3.3-70b-instruct", openai_client=openrouter_client)
oss_model = OpenAIChatCompletionsModel(model="openai/gpt-oss-120b", openai_client=groq_client)

sales_agent1 = Agent(name="Gemini Sales Agent", instructions=agent_instruction, model=gemini_model)
sales_agent2 = Agent(name="Llama Sales Agent", instructions=agent_instruction, model=llama_model)
sales_agent3 = Agent(name="GPT-OSS Sales Agent", instructions=agent_instruction, model=oss_model)

description = "Use this tool to write a sales email. In the input, just instruct it to write a sales email."

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

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

tools = [tool1, tool2, tool3, send_email_tool]


class EmailReview(BaseModel):
    is_professional: bool = Field(description="Whether the email is professional and appropriate.")
    number_of_sentences: int = Field(description="The number of sentences in the body of the email, not including the greeting and signature.")
    contains_placeholders: bool = Field(description="Whether the email contains placeholders for personalization.")

sales_manager = Agent(name="Sales Manager", instructions=manager_instruction, tools=tools, model="gpt-5.4-mini", output_type=EmailReview)
