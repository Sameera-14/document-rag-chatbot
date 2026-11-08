

import streamlit as st

from src.generation import generate_answer
from src.retrieval import retrieve_documents


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AeroPulse | Document RAG",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📚 AeroPulse RAG")

    st.caption("Document Intelligence Assistant")

    st.divider()

    st.subheader("About")

    st.write(
        "Ask questions about your indexed PDF documents. "
        "Answers are generated using retrieved document evidence."
    )

    st.divider()

    st.subheader("Features")

    st.markdown(
        """
        - 🔍 Semantic document retrieval
        - 📄 PDF-based answers
        - 📌 Source citations
        - 📖 Retrieved passage inspection
        - 🛡️ Evidence-based responses
        """
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.caption("AeroPulse RAG | Powered by ChromaDB")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("📚 AeroPulse Document RAG Chatbot")

st.write(
    "Ask questions about your knowledge-base documents "
    "and receive answers supported by PDF evidence."
)

st.divider()


# ============================================================
# WELCOME MESSAGE
# ============================================================

if not st.session_state.messages:

    st.info(
        "Welcome! Ask a question about your indexed PDF documents."
    )

    st.markdown("### Example questions")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            - What does bluejay mean?
            - What is the collection identifier?
            - How many approved learning notes are there?
            """
        )

    with col2:

        st.markdown(
            """
            - How many subject groups are there?
            - What is the chunk size?
            - What is the overlap?
            """
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask something about your documents..."
)


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if question:

    # Display user message.

    st.session_state.messages.append({

        "role": "user",

        "content": question

    })

    with st.chat_message("user"):

        st.markdown(question)

    # Generate assistant response.

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents and preparing your answer..."
        ):

            try:

                # Generate evidence-based answer.

                answer = generate_answer(
                    question,
                    use_rag=True
                )

                st.markdown("### Answer")

                st.markdown(answer)

                # Display retrieved document evidence.

                with st.expander(
                    "📄 View Retrieved Documents",
                    expanded=False
                ):

                    documents = retrieve_documents(
                        question,
                        top_k=4
                    )

                    if documents:

                        for index, document in enumerate(
                            documents,
                            start=1
                        ):

                            st.markdown(
                                f"#### Result {index}"
                            )

                            st.write(
                                "**Source:**",
                                document.get(
                                    "source",
                                    "Unknown"
                                )
                            )

                            st.write(
                                "**Page:**",
                                document.get(
                                    "page",
                                    "Unknown"
                                )
                            )

                            distance = document.get(
                                "distance"
                            )

                            if distance is not None:

                                st.write(
                                    "**Cosine distance:**",
                                    round(distance, 4)
                                )

                            st.markdown("**Content:**")

                            st.text(
                                document.get(
                                    "text",
                                    ""
                                )
                            )

                            st.divider()

                    else:

                        st.warning(
                            "No documents were retrieved."
                        )

            except Exception as error:

                answer = (
                    "An error occurred while processing "
                    "your question."
                )

                st.error(answer)

                st.exception(error)

    # Save assistant response.

    st.session_state.messages.append({

        "role": "assistant",

        "content": answer

    })
