# Multi agent workflow 

## Orchestrating by LLM(Tools)
Let create different sales agents. These agents create emails.

1. Agent 1 -> Gemini Sales Agent
2. Agent 2 -> Llama Sales Agent
3. Agent 3 -> GPT-OSS Sales Agent

Sales Manager Agent. Selects the best email from the available options and send the email
to potential customers.

Sales Manager Agent -> gpt-5.4-mini


## Flow
```mermaid
flowchart TD
	A[Task Prompt] --> B[Sales Manager gpt-5.4-mini]
	B --> C1[sales_agent1 Gemini]
	B --> C2[sales_agent2 Llama]
	B --> C3[sales_agent3 GPT OSS]
	C1 --> D[Draft 1]
	C2 --> E[Draft 2]
	C3 --> F[Draft 3]
	D --> G[Compare drafts and pick best]
	E --> G
	F --> G
	G --> H[send_email_tool]
	H --> I[EmailReview output]
```
