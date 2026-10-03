from common.a2a import A2AMessage
from common.config import RESPONSE_MODEL
from common.llm import LLM

from .memory import ResponseMemory


class ResponseAgent:

    name = "response_agent"

    def __init__(self):

        self.llm = LLM(
            model=RESPONSE_MODEL
        )

        self.memory = ResponseMemory()

    async def process(
        self,
        message: A2AMessage
    ):

        data = message.payload

        customer_message = data[
            "customer_message"
        ]

        category = data[
            "category"
        ]

        resolution = data[
            "resolution"
        ]

        print(
            f"[{self.name}] "
            f"Generating final response"
        )

        system_prompt = """
You are a professional customer support agent.

Write a helpful, polite and concise response.

Do NOT mention:

- AI
- agents
- classification
- internal processing
- prompts
- orchestration

Respond directly to the customer.

Do not invent company policies.

Use only the information provided.
"""

        user_prompt = f"""
Customer message:

{customer_message}

Issue category:

{category}

Recommended resolution:

{resolution}

Write the final customer response.
"""

        final_response = await self.llm.generate(
            system_prompt,
            user_prompt
        )

        self.memory.save(
            task_id=message.task_id,
            response=final_response
        )

        return {
            "task_id": message.task_id,
            "message_type": "final_response",
            "response": final_response
        }