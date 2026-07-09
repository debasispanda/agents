import asyncio
from agents import trace, Runner
from tools import sales_agent1, sales_agent2, sales_agent3, email_sender

async def start():
    message = "Write a cold sales email"

    with trace("Parallel cold sales emails"):
        results = await asyncio.gather(
            Runner.run(sales_agent1, message),
            Runner.run(sales_agent2, message),
            Runner.run(sales_agent3, message),
        )

    outputs = [result.final_output for result in results]
    
    emails = "Cold sales emails: \n\n" + "Email:\n\n".join(outputs)

    final_response = await Runner.run(email_sender, emails)

    print(f"Final Response: {final_response.final_output}")

if __name__ == "__main__":
    asyncio.run(start())
