
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts):

    if not texts:
        return []

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings.tolist()


if __name__ == "__main__":

    sample = [
        "What does bluejay mean?",
        "What is machine learning?"
    ]

    vectors = generate_embeddings(sample)

    print("Number of embeddings:", len(vectors))
    print("Embedding dimensions:", len(vectors[0]))
