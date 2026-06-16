from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-mpnet-base-v2"
)


def get_embedding(text):

    return model.encode(
        text,
        normalize_embeddings=True
    )