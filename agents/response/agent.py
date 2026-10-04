from common.a2a import (
    A2AMessage,
    send_message
)

from common.config import (
    RESPONSE_MODEL,
    EVALUATOR_URL
)

from common.llm import LLM

from .memory import ResponseMemory
from .tools import clean_response


class ResponseAgent:

    name = "response_agent"

    def __init__(self):

        self.llm = LLM(
            RESPONSE_MODEL
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

        policy = data[
            "policy"
        ]

        resolution = data[
            "resolution"
        ]

        retry_count = data.get(
            "retry_count",
            0
        )

        feedback = data.get(
            "feedback"
        )

        previous_response = data.get(
            "previous_response"
        )

        system_prompt = """
You are a professional customer support agent.

Generate a concise, helpful and polite
customer-facing response.

STRICT RULES:

1. Follow the supplied policy.
2. Follow the recommended resolution.
3. Never invent company policies.
4. Never guarantee refunds or replacements
   unless explicitly verified.
5. Never invent order, shipping or warranty data.
6. Do not mention AI, agents, prompts,
   evaluation or internal processing.
"""

        user_prompt = f"""
CUSTOMER MESSAGE:

{customer_message}

CATEGORY:

{category}

POLICY:

{policy}

RECOMMENDED RESOLUTION:

{resolution}
"""

        if feedback:

            user_prompt += f"""

PREVIOUS RESPONSE:

{previous_response}

EVALUATOR FEEDBACK:

{feedback}

Rewrite the response and correct every issue
identified by the evaluator.
"""

        response = await self.llm.generate(
            system_prompt,
            user_prompt
        )

        response = clean_response(
            response
        )

        self.memory.save({
            "task_id": message.task_id,
            "retry": retry_count,
            "response": response
        })

        print(
            f"[RESPONSE] Attempt {retry_count + 1}"
        )

        evaluation_message = A2AMessage(
            task_id=message.task_id,
            sender=self.name,
            receiver="evaluator_agent",
            message_type="evaluation_request",
            payload={
                "customer_message":
                    customer_message,

                "category":
                    category,

                "policy":
                    policy,

                "resolution":
                    resolution,

                "response":
                    response,

                "retry_count":
                    retry_count
            }
        )

        return await send_message(
            EVALUATOR_URL,
            evaluation_message
        )