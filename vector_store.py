

import json
from pathlib import Path

import chromadb

from src.embeddings import generate_embeddings


CHUNKS_FILE = Path("data/chunks.json")

DB_PATH = "chroma_db"

COLLECTION_NAME = "ai_ml_knowledge"


# Connect to persistent ChromaDB.
client = chromadb.PersistentClient(
    path=DB_PATH
)


# IMPORTANT:
# Never delete the collection during module import.
# Reuse the existing collection across Python executions.

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "hnsw:space": "cosine"
    }
)


def store_chunks():

    if not CHUNKS_FILE.exists():

        raise FileNotFoundError(
            "chunks.json not found. Run python -m src.ingest first."
        )

    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:

        chunks = json.load(file)

    if not chunks:

        raise ValueError("No chunks found.")

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        chunk["id"]
        for chunk in chunks
    ]

    metadatas = [
        chunk["metadata"]
        for chunk in chunks
    ]

    print("\nGenerating embeddings...")

    embeddings = generate_embeddings(texts)

    print("Generated embeddings:", len(embeddings))

    # Remove old records, but KEEP the collection.
    existing_ids = collection.get()["ids"]

    if existing_ids:

        collection.delete(
            ids=existing_ids
        )

    batch_size = 100

    for start in range(0, len(texts), batch_size):

        end = start + batch_size

        collection.upsert(

            ids=ids[start:end],

            documents=texts[start:end],

            metadatas=metadatas[start:end],

            embeddings=embeddings[start:end]

        )

    print("\n========== VECTOR STORE RESULTS ==========")

    print("Collection:", COLLECTION_NAME)

    print("Stored chunks:", collection.count())

    print("Database:", DB_PATH)

    return collection.count()


if __name__ == "__main__":

    store_chunks()
