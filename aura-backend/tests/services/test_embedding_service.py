import pytest
from app.services.embedding_service import embedding_service
import numpy as np

def test_embedding_service():
    """
    Tests that the EmbeddingService can create valid embeddings.
    """
    test_sentences = ["This is a test sentence.", "Here is another one."]
    embeddings = embedding_service.embed_texts(test_sentences)
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == 2
    
    # Check the first embedding
    assert isinstance(embeddings[0], list)
    assert len(embeddings[0]) == 384
    assert isinstance(embeddings[0][0], float) 