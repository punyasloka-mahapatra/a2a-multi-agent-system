import asyncio
import uuid

from common.a2a import (
    A2AMessage,
    send_message
)

from common.config import CLASSIFIER_URL


async def run():

    print("=" * 70)
    print("       A2A MULTI-AGENT CUSTOMER SUPPORT")
    print("=" * 70)

    customer_message = input(
        "\nEnter customer complaint:\n> "
    )

    task_id = str(uuid.uuid4())

    print(
        f"\nTask ID: {task_id}"
    )

    print(
        "\nCustomer"
        " → Classifier Agent"
    )

    message = A2AMessage(
        task_id=task_id,
        sender="customer",
        receiver="classifier_agent",
        message_type="customer_complaint",
        payload=customer_message
    )

    result = await send_message(
        CLASSIFIER_URL,
        message
    )

    print("\n")
    print("=" * 70)
    print("                    FINAL RESPONSE")
    print("=" * 70)

    print()

    if isinstance(result, dict):

        print(
            result.get(
                "response",
                result
            )
        )

    else:

        print(result)

    print()
    print("=" * 70)
    print("                    TASK COMPLETE")
    print("=" * 70)


if __name__ == "__main__":

    asyncio.run(run())