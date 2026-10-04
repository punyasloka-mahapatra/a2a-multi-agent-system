def clamp_score(value) -> float:

    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0

    return max(
        0.0,
        min(1.0, value)
    )


def calculate_score(
    evaluation: dict
) -> float:

    groundedness = clamp_score(
        evaluation.get(
            "groundedness",
            0
        )
    )

    policy = clamp_score(
        evaluation.get(
            "policy_compliance",
            0
        )
    )

    relevance = clamp_score(
        evaluation.get(
            "relevance",
            0
        )
    )

    completeness = clamp_score(
        evaluation.get(
            "completeness",
            0
        )
    )

    quality = clamp_score(
        evaluation.get(
            "response_quality",
            0
        )
    )

    return round(
        groundedness * 0.25
        + policy * 0.25
        + relevance * 0.20
        + completeness * 0.15
        + quality * 0.15,
        3
    )