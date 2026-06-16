from deduplicator import detect_duplicate

HIGH_THRESHOLD = 0.85
LOW_THRESHOLD = 0.65


def agent_loop(ticket, database):

    reasoning = []

    # Step 1: Search for similar tickets
    result = detect_duplicate(ticket, database)

    reasoning.append(
        f"Step 1: Semantic similarity = {round(result['score'], 2)}"
    )

    # Step 2: High confidence
    if result["score"] >= HIGH_THRESHOLD:

        reasoning.append(
            "Step 2: High confidence duplicate found"
        )

        return {
            "decision": "duplicate",
            "match": result["match"],
            "score": result["score"],
            "embedding": result["embedding"],
            "reasoning": reasoning
        }

    # Step 3: Medium confidence → second reasoning
    elif result["score"] >= LOW_THRESHOLD:

        reasoning.append(
            "Step 2: Medium confidence, checking keywords"
        )

        words1 = set(ticket.lower().split())
        words2 = set(result["match"]["ticket"].lower().split())

        overlap = len(words1.intersection(words2))

        reasoning.append(
            f"Step 3: Keyword overlap = {overlap}"
        )

        if overlap >= 2:

            reasoning.append(
                "Step 4: Duplicate confirmed"
            )

            return {
                "decision": "duplicate",
                "match": result["match"],
                "score": result["score"],
                "embedding": result["embedding"],
                "reasoning": reasoning
            }

    reasoning.append(
        "Step 4: New ticket created"
    )

    return {
        "decision": "new",
        "match": None,
        "score": result["score"],
        "embedding": result["embedding"],
        "reasoning": reasoning
    }