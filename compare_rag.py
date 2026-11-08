

from src.generation import generate_answer


def compare_rag(question):

    print("\n" + "=" * 65)

    print("             RAG vs WITHOUT RAG")

    print("=" * 65)

    print("\nQuestion:", question)

    print("\n========== WITHOUT RAG ==========")

    without_rag = generate_answer(
        question,
        use_rag=False
    )

    print(without_rag)

    print("\n========== WITH RAG ==========")

    with_rag = generate_answer(
        question,
        use_rag=True
    )

    print(with_rag)

    print("\n========== EVALUATION ==========")

    print("Without RAG: No private document context.")

    print("With RAG: Uses retrieved document chunks.")

    print("\nComparison completed.")

    return {
        "question": question,
        "without_rag": without_rag,
        "with_rag": with_rag
    }


if __name__ == "__main__":

    questions = [

        "What does bluejay mean?",

        "What is the collection identifier?",

        "How many approved learning notes are there?"

    ]

    for question in questions:

        compare_rag(question)
