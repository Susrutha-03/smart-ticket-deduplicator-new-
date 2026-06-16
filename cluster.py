from database import get_all_tickets
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

CLUSTER_THRESHOLD = 0.75


def build_clusters():

    tickets = get_all_tickets()

    clusters = []
    visited = set()

    for i in range(len(tickets)):

        if i in visited:
            continue

        current_cluster = [tickets[i]]
        visited.add(i)

        emb1 = np.array(tickets[i]["embedding"])

        for j in range(i + 1, len(tickets)):

            if j in visited:
                continue

            emb2 = np.array(tickets[j]["embedding"])

            similarity = cosine_similarity(
                [emb1],
                [emb2]
            )[0][0]

            if similarity >= CLUSTER_THRESHOLD:
                current_cluster.append(tickets[j])
                visited.add(j)

        clusters.append(current_cluster)

    return clusters