

from src.embeddings import generate_embeddings
from src.vector_store import collection


def retrieve_documents(question, top_k=4):

    if not question or not question.strip():
        return []

    total = collection.count()

    if total == 0:

        raise RuntimeError(
            "ChromaDB is empty. Run ingestion and vector storage first."
        )

    top_k = min(top_k, total)

    query_embedding = generate_embeddings(
        [question]
    )[0]

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]

    )

    retrieved_documents = []

    if not results["documents"]:
        return []

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]

        distance = results["distances"][0][i]

        retrieved_documents.append({

            "text": document,

            "source": metadata.get("source", "Unknown"),

            "page": metadata.get("page", "Unknown"),

            "chunk": metadata.get("chunk", 0),

            "distance": distance

        })

    return retrieved_documents


def get_context(documents):

    return "\n\n".join(
        document["text"]
        for document in documents
    )


def display_retrieved_documents(documents):

    print("\n========== RETRIEVED DOCUMENTS ==========")

    for index, document in enumerate(documents, start=1):

        print(f"\nResult {index}")

        print("Source:", document["source"])

        print("Page:", document["page"])

        print("Chunk:", document["chunk"])

        print("Distance:", round(document["distance"], 4))

        print("Content:", document["text"])


if __name__ == "__main__":

    question = input("Enter your question: ")

    results = retrieve_documents(question)

    display_retrieved_documents(results)
