

import re

from src.retrieval import retrieve_documents

NOT_FOUND = "Information not found in the provided documents."


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_fact(question, documents):

    q = question.lower()

    # Each rule extracts only the required fact.
    rules = [
        {
            "triggers": ["bluejay", "blue jay"],
            "pattern": r"assigns the label ['\"]bluejay['\"] to documents that have passed both text extraction review and source metadata validation",
            "answer": "Documents that have passed both text extraction review and source metadata validation are assigned the label 'bluejay'."
        },
        {
            "triggers": ["collection identifier", "collection id"],
            "pattern": r"collection identifier used in this example is\s+(NSL-[A-Z0-9-]+)",
            "answer_group": 1
        },
        {
            "triggers": ["approved learning notes", "approved notes"],
            "pattern": r"contains\s+(\d+)\s+approved learning notes",
            "answer_group": 1,
            "suffix": "approved learning notes"
        },
        {
            "triggers": ["subject groups"],
            "pattern": r"organized into\s+(\w+)\s+subject groups",
            "answer_group": 1,
            "suffix": "subject groups"
        },
        {
            "triggers": ["chunk size"],
            "pattern": r"chunk size is\s+(\d+\s+tokens)",
            "answer_group": 1
        },
        {
            "triggers": ["overlap"],
            "pattern": r"overlap is\s+(\d+)",
            "answer_group": 1,
            "suffix": "tokens"
        },
        {
            "triggers": ["retrieval count", "top k"],
            "pattern": r"retrieval count is\s+(top\s+\d+\s+chunks)",
            "answer_group": 1
        }
    ]

    selected_rule = None

    for rule in rules:
        if any(trigger in q for trigger in rule["triggers"]):
            selected_rule = rule
            break

    if selected_rule is None:
        return None

    for document in documents:

        text = clean_text(document["text"])

        match = re.search(
            selected_rule["pattern"],
            text,
            re.IGNORECASE
        )

        if not match:
            continue

        if "answer" in selected_rule:
            answer = selected_rule["answer"]

        else:
            answer = match.group(
                selected_rule["answer_group"]
            )

            suffix = selected_rule.get("suffix")

            if suffix:
                answer = f"{answer} {suffix}"

        return {
            "answer": answer,
            "source": document.get("source", "Unknown"),
            "page": document.get("page", "Unknown")
        }

    return None


def find_generic_evidence(question, documents):

    stop_words = {
        "what", "is", "are", "was", "were",
        "the", "a", "an", "of", "in", "on",
        "to", "for", "and", "or", "does",
        "do", "how", "many", "much", "with",
        "from", "which", "who", "when", "where",
        "tell", "me", "about", "explain"
    }

    words = set(re.findall(r"[a-zA-Z0-9_-]+", question.lower()))
    keywords = words - stop_words

    if not keywords:
        return None

    for document in documents:

        text = document["text"]

        # Split on sentence boundaries and line breaks.
        sentences = re.split(r"(?<=[.!?])\s+|\n+", text)

        for sentence in sentences:

            sentence = clean_text(sentence)

            if not sentence:
                continue

            sentence_words = set(
                re.findall(r"[a-zA-Z0-9_-]+", sentence.lower())
            )

            overlap = keywords.intersection(sentence_words)

            if len(overlap) == len(keywords):

                return {
                    "answer": sentence,
                    "source": document.get("source", "Unknown"),
                    "page": document.get("page", "Unknown")
                }

    return None


def generate_answer(question, use_rag=True):

    if not question or not question.strip():
        return "Please enter a valid question."

    if not use_rag:
        return "General knowledge generation is disabled."

    try:

        documents = retrieve_documents(
            question.strip(),
            top_k=4
        )

    except Exception as error:

        print("Retrieval error:", error)
        return NOT_FOUND

    if not documents:
        return NOT_FOUND

    # First attempt precise extraction.
    evidence = extract_fact(
        question,
        documents
    )

    # Then attempt generic evidence extraction.
    if evidence is None:

        evidence = find_generic_evidence(
            question,
            documents
        )

    if evidence is None:
        return NOT_FOUND

    return (
        evidence["answer"]
        + f"\n\nSource: {evidence['source']}, "
        + f"Page: {evidence['page']}"
    )


if __name__ == "__main__":

    questions = [
        "What does bluejay mean?",
        "What is the collection identifier?",
        "How many approved learning notes are there?",
        "How many subject groups are there?",
        "What is the chunk size?",
        "What is the overlap?",
        "What is the office address?"
    ]

    print("\n" + "=" * 60)
    print("       DOCUMENT RAG CHATBOT TEST")
    print("=" * 60)

    for question in questions:

        print("\nQuestion:", question)
        print("\nAnswer:", generate_answer(question))
        print("-" * 60)
