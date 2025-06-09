"""
Unit tests for RAG service operations (P5-T3).
"""

import os
import pytest
from uuid import uuid4
from unittest.mock import Mock, patch, MagicMock

# Ensure testing environment is set before any app imports
os.environ["TESTING"] = "true"

from app.services.rag_service import RAGService, RAGResponse, generate_rag_answer


class TestRAGService:
    """Test suite for RAG service functionality."""
    
    def test_rag_service_initialization(self):
        """Test RAG service initialization with default and custom parameters."""
        # Test default initialization
        service = RAGService()
        assert service.model == "gpt-3.5-turbo"
        assert service.max_chunks == 5
        assert service.max_tokens == 1000
        assert service.temperature == 0.3
        
        # Test custom initialization
        custom_service = RAGService(
            model="gpt-4",
            max_chunks=10,
            max_tokens=2000,
            temperature=0.7
        )
        assert custom_service.model == "gpt-4"
        assert custom_service.max_chunks == 10
        assert custom_service.max_tokens == 2000
        assert custom_service.temperature == 0.7
    
    @patch('app.services.rag_service.query_vector_store')
    @patch('app.services.rag_service.litellm.completion')
    def test_generate_answer_success(self, mock_completion, mock_query):
        """Test successful answer generation with retrieved chunks."""
        test_document_id = uuid4()
        
        # Mock vector store response
        mock_chunks = [
            {
                'text': 'Machine learning is a subset of artificial intelligence.',
                'metadata': {'document_id': str(test_document_id), 'chunk_index': 1},
                'distance': 0.1
            },
            {
                'text': 'Neural networks are inspired by biological neural networks.',
                'metadata': {'document_id': str(test_document_id), 'chunk_index': 3},
                'distance': 0.2
            }
        ]
        mock_query.return_value = mock_chunks
        
        # Mock LLM response
        mock_llm_response = Mock()
        mock_llm_response.choices = [Mock()]
        mock_llm_response.choices[0].message.content = "Machine learning is a subset of AI that uses neural networks."
        mock_completion.return_value = mock_llm_response
        
        # Create service and generate answer
        service = RAGService()
        question = "What is machine learning?"
        result = service.generate_answer(question, test_document_id)
        
        # Verify vector store was called correctly
        mock_query.assert_called_once_with(
            query_text=question,
            document_id=test_document_id,
            n_results=5
        )
        
        # Verify LLM was called with correct parameters
        mock_completion.assert_called_once()
        call_args = mock_completion.call_args
        assert call_args[1]['model'] == 'gpt-3.5-turbo'
        assert call_args[1]['max_tokens'] == 1000
        assert call_args[1]['temperature'] == 0.3
        assert len(call_args[1]['messages']) == 2
        
        # Verify system message
        system_message = call_args[1]['messages'][0]
        assert system_message['role'] == 'system'
        assert 'helpful assistant' in system_message['content']
        
        # Verify user message contains question and context
        user_message = call_args[1]['messages'][1]
        assert user_message['role'] == 'user'
        assert question in user_message['content']
        assert 'Machine learning is a subset' in user_message['content']
        assert 'Neural networks are inspired' in user_message['content']
        
        # Verify response
        assert isinstance(result, RAGResponse)
        assert result.answer == "Machine learning is a subset of AI that uses neural networks."
        assert len(result.chunks_used) == 2
        assert result.chunks_used == mock_chunks
    
    @patch('app.services.rag_service.query_vector_store')
    def test_generate_answer_no_chunks_found(self, mock_query):
        """Test handling when no relevant chunks are found."""
        test_document_id = uuid4()
        
        # Mock empty vector store response
        mock_query.return_value = []
        
        service = RAGService()
        result = service.generate_answer("What is quantum computing?", test_document_id)
        
        # Verify response for no chunks
        assert isinstance(result, RAGResponse)
        assert "couldn't find any relevant information" in result.answer
        assert len(result.chunks_used) == 0
    
    @patch('app.services.rag_service.query_vector_store')
    @patch('app.services.rag_service.litellm.completion')
    def test_generate_answer_with_custom_n_results(self, mock_completion, mock_query):
        """Test generate_answer with custom n_results parameter."""
        test_document_id = uuid4()
        
        mock_query.return_value = []
        mock_llm_response = Mock()
        mock_llm_response.choices = [Mock()]
        mock_llm_response.choices[0].message.content = "Test response"
        mock_completion.return_value = mock_llm_response
        
        service = RAGService()
        service.generate_answer("test question", test_document_id, n_results=3)
        
        # Verify custom n_results was passed to query_vector_store
        mock_query.assert_called_once_with(
            query_text="test question",
            document_id=test_document_id,
            n_results=3
        )
    
    @patch('app.services.rag_service.query_vector_store')
    @patch('app.services.rag_service.litellm.completion')
    def test_generate_answer_llm_error_handling(self, mock_completion, mock_query):
        """Test error handling when LLM call fails."""
        test_document_id = uuid4()
        
        # Mock successful vector store response
        mock_query.return_value = [
            {
                'text': 'Some content',
                'metadata': {'document_id': str(test_document_id), 'chunk_index': 1},
                'distance': 0.1
            }
        ]
        
        # Mock LLM error
        mock_completion.side_effect = Exception("API rate limit exceeded")
        
        service = RAGService()
        result = service.generate_answer("test question", test_document_id)
        
        # Verify error is handled gracefully
        assert isinstance(result, RAGResponse)
        assert "error while processing" in result.answer.lower()
        assert "API rate limit exceeded" in result.answer
        assert len(result.chunks_used) == 0
    
    def test_construct_prompt(self):
        """Test prompt construction with multiple chunks."""
        service = RAGService()
        
        question = "What is artificial intelligence?"
        chunks = [
            {
                'text': 'AI is intelligence demonstrated by machines.',
                'metadata': {'chunk_index': 1},
                'distance': 0.1
            },
            {
                'text': 'Machine learning is a subset of AI.',
                'metadata': {'chunk_index': 3},
                'distance': 0.2
            }
        ]
        
        prompt = service._construct_prompt(question, chunks)
        
        # Verify prompt structure
        assert question in prompt
        assert 'AI is intelligence demonstrated by machines.' in prompt
        assert 'Machine learning is a subset of AI.' in prompt
        assert '[Context 1 - Chunk 1]' in prompt
        assert '[Context 2 - Chunk 3]' in prompt
        assert 'Answer based only on the provided context' in prompt
    
    def test_construct_prompt_with_missing_metadata(self):
        """Test prompt construction when chunk metadata is incomplete."""
        service = RAGService()
        
        question = "Test question?"
        chunks = [
            {
                'text': 'Some text content',
                'metadata': {},  # Missing chunk_index
                'distance': 0.1
            }
        ]
        
        prompt = service._construct_prompt(question, chunks)
        
        # Should handle missing metadata gracefully
        assert question in prompt
        assert 'Some text content' in prompt
        assert '[Context 1 - Chunk unknown]' in prompt


class TestRAGServiceConvenienceFunction:
    """Test the convenience function for RAG operations."""
    
    @patch('app.services.rag_service.RAGService')
    def test_generate_rag_answer_convenience_function(self, mock_service_class):
        """Test the convenience function creates service and calls generate_answer."""
        mock_service = Mock()
        mock_service_class.return_value = mock_service
        mock_response = RAGResponse(answer="Test answer", chunks_used=[])
        mock_service.generate_answer.return_value = mock_response
        
        test_document_id = uuid4()
        question = "Test question"
        
        result = generate_rag_answer(
            question=question,
            document_id=test_document_id,
            model="gpt-4",
            n_results=3
        )
        
        # Verify service was created with correct parameters
        mock_service_class.assert_called_once_with(model="gpt-4", max_chunks=3)
        
        # Verify generate_answer was called correctly
        mock_service.generate_answer.assert_called_once_with(question, test_document_id, 3)
        
        # Verify response
        assert result == mock_response 