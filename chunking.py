
import tiktoken


ENCODING = tiktoken.get_encoding("cl100k_base")

CHUNK_SIZE = 420
CHUNK_OVERLAP = 60


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):

    if not text or not text.strip():
        return []

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap.")

    tokens = ENCODING.encode(text)

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(tokens), step):

        end = min(start + chunk_size, len(tokens))

        chunk_tokens = tokens[start:end]

        chunk = ENCODING.decode(chunk_tokens).strip()

        if chunk:
            chunks.append(chunk)

        if end == len(tokens):
            break

    return chunks


if __name__ == "__main__":

    sample = "This is a sample document. " * 500

    chunks = chunk_text(sample)

    print("Total chunks:", len(chunks))

    for i, chunk in enumerate(chunks[:3], start=1):

        print(f"\nChunk {i}")

        print("Token count:", len(ENCODING.encode(chunk)))

        print(chunk[:200])
