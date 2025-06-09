from typing import List
import pathlib

def process_document(file_path: str) -> List[str]:
    """
    Reads a document, extracts its text, and splits it into chunks.
    Currently supports .txt and .md files.
    """
    path = pathlib.Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"No file found at {file_path}")

    # For MVP, we assume text-based files. A more robust solution would handle
    # different file types (e.g., .pdf, .docx) with appropriate libraries.
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        # Broad exception to catch potential decoding errors
        raise IOError(f"Could not read file {file_path}: {e}")

    return chunk_text(text)


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> List[str]:
    """
    Splits a long text into smaller chunks with a specified overlap.

    Args:
        text: The input text to be chunked.
        chunk_size: The desired maximum size of each chunk (in characters).
        chunk_overlap: The number of characters to overlap between consecutive chunks.

    Returns:
        A list of text chunks.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    chunks = []
    start_index = 0
    while start_index < len(text):
        end_index = start_index + chunk_size
        chunks.append(text[start_index:end_index])
        start_index += chunk_size - chunk_overlap
            
    return chunks 