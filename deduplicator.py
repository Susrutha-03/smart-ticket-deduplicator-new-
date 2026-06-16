import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embedding import get_embedding

# Lower threshold for better semantic matching
SIMILARITY_THRESHOLD = 0.75


def detect_duplicate(ticket, database):

    # Generate embedding for new ticket
    new_embedding = get_embedding(ticket)

    # If database is empty
    if len(database) == 0:
        return {
            "duplicate": False,
            "score": 0,
            "match": None,
            "embedding": new_embedding
        }

    best_score = -1
    best_ticket = None

    # Compare with every existing ticket
    for item in database:

        existing_embedding = np.array(item["embedding"])

        score = cosine_similarity(
            [new_embedding],
            [existing_embedding]
        )[0][0]

        # Debug: print similarity scores
        print("=" * 50)
        print("New Ticket:", ticket)
        print("Existing Ticket:", item["ticket"])
        print("Similarity:", round(score, 3))
        print("=" * 50)

        if score > best_score:
            best_score = score
            best_ticket = item

    print("Best Match:", best_ticket["ticket"])
    print("Best Score:", best_score)

    return {
        "duplicate": best_score >= SIMILARITY_THRESHOLD,
        "score": best_score,
        "match": best_ticket,
        "embedding": new_embedding
    }