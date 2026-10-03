import uuid

from common.a2a import A2AMessage, send_message
from common.config import (
    CLASSIFIER_MODEL,
    RESOLUTION_URL
)
from common.llm import LLM

from .memory import ClassifierMemory


class ClassifierAgent:

    name = "classifier_agent"

    def __init__(self):

        self.llm = LLM(
            model=CLASSIFIER_MODEL
        )

        self.memory = ClassifierMemory()

    async def process(
        self,
        message: A2AMessage
    ):

        customer_message = message.payload

        print(
            f"[{self.name}] "
            f"Processing task {message.task_id}"
        )

        system_prompt = """
You are a customer support classification agent.

Classify the customer complaint into exactly
one of these categories:

product_issue
refund_request
delivery_issue
general_question

Return ONLY the category name.
Do not explain your answer.
"""

        category = await self.llm.generate(
            system_prompt,
            customer_message
        )

        category = category.lower().strip()

        valid_categories = {
            "product_issue",
            "refund_request",
            "delivery_issue",
            "general_question"
        }

        if category not in valid_categories:
            category = "general_question"

        # Agent-specific memory
        self.memory.save(
            task_id=message.task_id,
            customer_message=customer_message,
            category=category
        )

        print(
            f"[{self.name}] "
            f"Category = {category}"
        )

        next_message = A2AMessage(
            task_id=message.task_id,
            sender=self.name,
            receiver="resolution_agent",
            message_type="classification_result",
            payload={
                "customer_message": customer_message,
                "category": category
            }
        )

        return await send_message(
            RESOLUTION_URL,
            next_message
        )