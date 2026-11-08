# 🚀 Document RAG Chatbot

AI-powered Document Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about PDF documents and receive context-aware answers with source references.

The system combines semantic search, vector database retrieval, and AI-based answer generation to provide accurate and relevant responses from uploaded knowledge-base documents.

## ✨ Features

- 📄 PDF document ingestion and text extraction.
- ✂️ Text chunking for efficient document processing.
- 🧠 Semantic embeddings for document representation.
- 🗄️ ChromaDB vector database for storing and retrieving document embeddings.
- 🔍 Similarity-based document retrieval.
- 🤖 FLAN-T5 based answer generation.
- 📚 Source filename and PDF page number citations.
- 🚫 Handles questions when information is unavailable in the documents.
- 💬 Interactive Streamlit chatbot interface.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| ChromaDB | Vector database |
| Sentence Transformers | Text embeddings |
| FLAN-T5 | Answer generation |
| PyMuPDF | PDF text extraction |

## 📁 Project Structure

```text
document-rag-chatbot/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── chunking.py
│   ├── compare_rag.py
│   ├── embeddings.py
│   ├── generation.py
│   ├── ingest.py
│   ├── retrieval.py
│   └── vector_store.py
│
└── data/
    └── AI_ML_Knowledge_Base_Guide.pdf
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd document-rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔄 RAG Workflow

1. **Document Ingestion:** PDF documents are loaded and text is extracted.
2. **Chunking:** Extracted text is divided into smaller chunks.
3. **Embedding Generation:** Text chunks are converted into numerical embeddings.
4. **Vector Storage:** Embeddings and metadata are stored in ChromaDB.
5. **Retrieval:** Relevant document chunks are retrieved based on the user's question.
6. **Answer Generation:** FLAN-T5 generates an answer using the retrieved context.
7. **Source Citation:** The answer includes the source PDF filename and page number.

## 🧪 Sample Questions

| Question | Expected Answer |
|---|---|
| What does bluejay mean? | Documents that pass text extraction review and source metadata validation. |
| What is the collection identifier? | NSL-AURORA-36 |
| How many approved learning notes are there? | 36 approved learning notes |
| How many subject groups are there? | Six subject groups |
| What is the office address? | Information not found in the provided documents. |

## 🎯 Project Objective

The objective of AeroPulse is to demonstrate how Retrieval-Augmented Generation can improve document-based question answering by combining semantic search with language generation.

The chatbot focuses on providing answers grounded in the available documents rather than generating unsupported information.

## 👨‍💻 Author

Developed as an AI/ML project using Python, NLP, Vector Databases, and Retrieval-Augmented Generation.

---

⭐ If you find this project interesting, feel free to explore the repository!
