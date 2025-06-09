"""
RAG (Retrieval-Augmented Generation) service for Aura (P5-T3).
"""

import logging
from typing import List, Dict, Any, Optional
from uuid import UUID

import litellm
from pydantic import BaseModel

from .vector_query_service import query_vector_store


logger = logging.getLogger(__name__)


class RAGResponse(BaseModel):
    """Response model for RAG operations."""
    answer: str
    chunks_used: List[Dict[str, Any]]


class RAGService:
    """RAG service that combines retrieval with generation."""
    
    def __init__(self, model: str = "gpt-3.5-turbo", max_chunks: int = 5):
        self.model = model
        self.max_chunks = max_chunks
    
    def generate_answer(self, question: str, document_id: UUID) -> RAGResponse:
        """Generate an answer to a question based on document content."""
        try:
            # Step 1: Retrieve relevant chunks
            chunks = query_vector_store(
                query_text=question,
                document_id=document_id,
                n_results=self.max_chunks
            )
            
            if not chunks:
                return RAGResponse(
                    answer="I couldn't find any relevant information in the document.",
                    chunks_used=[]
                )
            
            # Step 2: Construct prompt
            prompt = self._construct_prompt(question, chunks)
            
            # Step 3: Generate answer using LLM
            response = litellm.completion(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content.strip()
            
            return RAGResponse(answer=answer, chunks_used=chunks)
            
        except Exception as e:
            logger.error(f"RAG error: {str(e)}")
            return RAGResponse(
                answer=f"Error processing question: {str(e)}",
                chunks_used=[]
            )
    
    def _construct_prompt(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        """Construct a prompt with question and chunks."""
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            text = chunk.get('text', '')
            context_parts.append(f"Context {i}: {text}")
        
        context = "\n".join(context_parts)
        
        return f"""Based on this context, answer the question:

{context}

Question: {question}

Answer:"""


def generate_rag_answer(question: str, document_id: UUID) -> RAGResponse:
    """Convenience function to generate a RAG answer."""
    service = RAGService()
    return service.generate_answer(question, document_id) 