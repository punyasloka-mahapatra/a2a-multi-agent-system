import json

from common.a2a import (
    A2AMessage,
    send_message
)

from common.config import (
    EVALUATOR_MODEL,
    RESPONSE_URL,
    EVALUATION_THRESHOLD,
    MAX_RETRIES
)

from common.llm import LLM

from .memory import EvaluatorMemory
from .tools import calculate_score


class EvaluatorAgent:

    name = "evaluator_agent"

    def __init__(self):

        self.llm = LLM(
            EVALUATOR_MODEL
        )

        self.memory = EvaluatorMemory()

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

        response = data[
            "response"
        ]

        retry_count = data.get(
            "retry_count",
            0
        )

        system_prompt = """
You are an independent evaluator.

Evaluate the customer-support response.

Score each dimension between 0 and 1.

groundedness:
Does the response avoid unsupported claims?

policy_compliance:
Does it follow the supplied policy?

relevance:
Does it address the customer's problem?

completeness:
Does it sufficiently address the request?

response_quality:
Is it clear, concise, professional and helpful?

Be strict.

Return ONLY valid JSON.

Schema:

{
  "groundedness": 0.0,
  "policy_compliance": 0.0,
  "relevance": 0.0,
  "completeness": 0.0,
  "response_quality": 0.0,
  "issues": [],
  "feedback": ""
}
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

RESPONSE TO EVALUATE:

{response}
"""

        raw_result = await self.llm.generate(
            system_prompt,
            user_prompt
        )

        try:

            cleaned = (
                raw_result
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

            evaluation = json.loads(
                cleaned
            )

        except Exception:

            evaluation = {
                "groundedness": 0,
                "policy_compliance": 0,
                "relevance": 0,
                "completeness": 0,
                "response_quality": 0,
                "issues": [
                    "Evaluator returned invalid JSON."
                ],
                "feedback":
                    "Regenerate a conservative, "
                    "policy-grounded response."
            }

        score = calculate_score(
            evaluation
        )

        approved = (
            score >= EVALUATION_THRESHOLD
        )

        self.memory.save({
            "task_id": message.task_id,
            "retry": retry_count,
            "score": score,
            "approved": approved,
            "evaluation": evaluation
        })

        print(
            f"[EVALUATOR] Score: {score}"
        )

        print(
            f"[EVALUATOR] Approved: {approved}"
        )

        # PASS
        if approved:

            return {
                "task_id":
                    message.task_id,

                "status":
                    "approved",

                "score":
                    score,

                "attempts":
                    retry_count + 1,

                "response":
                    response,

                "evaluation":
                    evaluation
            }

        # RETRY
        if retry_count < MAX_RETRIES:

            print(
                "[EVALUATOR] "
                "Sending feedback to Response Agent"
            )

            retry_message = A2AMessage(
                task_id=message.task_id,
                sender=self.name,
                receiver="response_agent",
                message_type="optimization_feedback",
                payload={
                    "customer_message":
                        customer_message,

                    "category":
                        category,

                    "policy":
                        policy,

                    "resolution":
                        resolution,

                    "previous_response":
                        response,

                    "feedback":
                        evaluation.get(
                            "feedback",
                            "Improve the response."
                        ),

                    "retry_count":
                        retry_count + 1
                }
            )

            return await send_message(
                RESPONSE_URL,
                retry_message
            )

        # Maximum retries reached.
        return {
            "task_id":
                message.task_id,

            "status":
                "max_retries_reached",

            "score":
                score,

            "attempts":
                retry_count + 1,

            "response":
                response,

            "evaluation":
                evaluation
        }