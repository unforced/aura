"""
Vector store query operations for retrieving text chunks.
"""

from typing import List, Dict, Any
from uuid import UUID
from app.services.vector_store_service import VectorStoreService
from app.core.config import settings


def query_vector_store(query_text: str, document_id: UUID, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Query the vector store for the most relevant text chunks for a given document.
    
    This is the main function specified in P5-T2 for retrieving text chunks
    from the vector store based on a query text and document ID.
    
    Args:
        query_text: The text to search for semantically similar chunks
        document_id: UUID of the document to search within
        n_results: Maximum number of results to return (default: 5)
        
    Returns:
        List of dictionaries containing:
        - 'text': The text content of the chunk
        - 'metadata': Metadata associated with the chunk
        - 'distance': Semantic distance/similarity score
        
    Example:
        chunks = query_vector_store("What is the project about?", document_uuid)
        for chunk in chunks:
            print(f"Text: {chunk['text'][:100]}...")
            print(f"Distance: {chunk['distance']}")
    """
    # Initialize the vector store service
    vector_service = VectorStoreService(
        host=settings.CHROMA_HOST,
        port=settings.CHROMA_PORT
    )
    
    # Query for relevant chunks
    return vector_service.query_chunks(
        query_text=query_text,
        document_id=document_id,
        n_results=n_results
    ) 