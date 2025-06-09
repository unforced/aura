import pytest
from app.services.document_processing_service import chunk_text

def test_chunk_text_simple():
    """
    Tests the basic functionality of the text chunking function.
    """
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=3)
    
    assert len(chunks) == 4
    assert chunks[0] == "abcdefghij"
    assert chunks[1] == "hijklmnopq"
    assert chunks[2] == "opqrstuvwx"
    assert chunks[3] == "vwxyz"
    
def test_chunk_text_no_overlap():
    """
    Tests text chunking with no overlap.
    """
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text(text, chunk_size=10, chunk_overlap=0)
    
    assert len(chunks) == 3
    assert chunks[0] == "abcdefghij"
    assert chunks[1] == "klmnopqrst"
    assert chunks[2] == "uvwxyz"

def test_chunk_text_invalid_overlap():
    """
    Tests that an invalid overlap value raises a ValueError.
    """
    text = "some text"
    with pytest.raises(ValueError, match="chunk_overlap must be smaller than chunk_size."):
        chunk_text(text, chunk_size=10, chunk_overlap=10)
    
    with pytest.raises(ValueError, match="chunk_overlap must be smaller than chunk_size."):
        chunk_text(text, chunk_size=10, chunk_overlap=11) 