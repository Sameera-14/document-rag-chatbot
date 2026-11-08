
import json
from pathlib import Path

from pypdf import PdfReader

from src.chunking import chunk_text


DOCUMENTS_DIR = Path("documents")
DATA_DIR = Path("data")
CHUNKS_FILE = DATA_DIR / "chunks.json"


def extract_pdf(file_path):

    reader = PdfReader(str(file_path))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        if text.strip():

            documents.append({
                "text": text,
                "source": file_path.name,
                "page": page_number
            })

    return documents


def ingest_documents():

    DOCUMENTS_DIR.mkdir(exist_ok=True)
    DATA_DIR.mkdir(exist_ok=True)

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF documents found in documents/."
        )

    all_chunks = []

    for pdf_file in pdf_files:

        print(f"\nProcessing: {pdf_file.name}")

        pages = extract_pdf(pdf_file)

        print("Extracted pages:", len(pages))

        for page in pages:

            chunks = chunk_text(page["text"])

            for chunk_index, chunk in enumerate(chunks):

                all_chunks.append({

                    "id": (
                        f"{pdf_file.stem}_"
                        f"page_{page['page']}_"
                        f"chunk_{chunk_index}"
                    ),

                    "text": chunk,

                    "metadata": {
                        "source": page["source"],
                        "page": page["page"],
                        "chunk": chunk_index
                    }

                })

    if not all_chunks:
        raise ValueError("No text could be extracted from PDFs.")

    with open(CHUNKS_FILE, "w", encoding="utf-8") as file:

        json.dump(
            all_chunks,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\n========== INGESTION RESULTS ==========")

    print("PDF files:", len(pdf_files))
    print("Total chunks:", len(all_chunks))
    print("Saved to:", CHUNKS_FILE)

    return all_chunks


if __name__ == "__main__":

    ingest_documents()
