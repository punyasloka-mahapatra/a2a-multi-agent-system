POLICIES = {

    "product_issue": """
If the product appears defective,
recommend a replacement eligibility review.
Do not guarantee a replacement.
""",

    "refund_request": """
Recommend a refund eligibility review.
Do not guarantee a refund unless eligibility
has been verified.
""",

    "delivery_issue": """
Recommend investigation by the delivery team.
Do not claim the package is lost unless verified.
""",

    "general_question": """
Provide appropriate guidance.
Escalate to human support when required.
"""
}


def get_policy(category: str) -> str:

    return POLICIES.get(
        category,
        POLICIES["general_question"]
    )