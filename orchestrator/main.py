import asyncio
import uuid

from common.a2a import (
    A2AMessage,
    send_message
)

from common.config import CLASSIFIER_URL


async def run():

    print()
    print("=" * 70)
    print("       A2A SELF-EVALUATING MULTI-AGENT SYSTEM")
    print("=" * 70)

    customer_message = input(
        "\nEnter customer complaint:\n> "
    )

    task_id = str(
        uuid.uuid4()
    )

    print(
        f"\nTask ID: {task_id}"
    )

    initial_message = A2AMessage(
        task_id=task_id,
        sender="customer",
        receiver="classifier_agent",
        message_type="customer_complaint",
        payload=customer_message
    )

    result = await send_message(
        CLASSIFIER_URL,
        initial_message
    )

    print()
    print("=" * 70)
    print("                     RESULT")
    print("=" * 70)

    print(
        f"\nStatus: {result['status']}"
    )

    print(
        f"Evaluation Score: {result['score']}"
    )

    print(
        f"Attempts: {result['attempts']}"
    )

    print("\nFinal Response:\n")

    print(
        result["response"]
    )

    print()

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run())