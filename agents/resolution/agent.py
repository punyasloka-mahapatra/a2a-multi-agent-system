import uuid

from common.a2a import A2AMessage, send_message
from common.config import (
    RESOLUTION_MODEL,
    RESPONSE_URL
)
from common.llm import LLM

from .memory import ResolutionMemory


class ResolutionAgent:

    name = "resolution_agent"

    def __init__(self):

        self.llm = LLM(
            model=RESOLUTION_MODEL
        )

        self.memory = ResolutionMemory()

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

        print(
            f"[{self.name}] "
            f"Received category: {category}"
        )

        system_prompt = """
You are a customer support resolution agent.

Determine the appropriate next action.

Policies:

1. Product issues:
   Recommend replacement if the product
   appears defective.

2. Refund requests:
   Recommend refund review if the request
   is within the applicable return period.

3. Delivery issues:
   Recommend investigation by the
   delivery team.

4. General questions:
   Provide guidance or recommend human
   support if necessary.

Return a concise resolution.

Do not write the final customer response.
"""

        user_prompt = f"""
Customer complaint:

{customer_message}

Category:

{category}

Determine the recommended resolution.
"""

        resolution = await self.llm.generate(
            system_prompt,
            user_prompt
        )

        self.memory.save(
            task_id=message.task_id,
            category=category,
            resolution=resolution
        )

        print(
            f"[{self.name}] "
            f"Resolution generated"
        )

        next_message = A2AMessage(
            task_id=message.task_id,
            sender=self.name,
            receiver="response_agent",
            message_type="resolution_result",
            payload={
                "customer_message": customer_message,
                "category": category,
                "resolution": resolution
            }
        )

        return await send_message(
            RESPONSE_URL,
            next_message
        )