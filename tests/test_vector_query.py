"""
Unit tests for vector store query operations (P5-T2).
"""

import os
import pytest
from uuid import uuid4, UUID
from unittest.mock import Mock, patch

# Ensure testing environment is set before any app imports
os.environ["TESTING"] = "true"

from app.services.vector_query_service import query_vector_store
from app.core.config import settings


class TestVectorQuery:
    """Test suite for vector store query functionality."""
    
    def test_query_vector_store_basic_functionality(self):
        """Test basic query functionality returns results."""
        test_document_id = uuid4()
        
        # Mock the VectorStoreService
        with patch('app.services.vector_query_service.VectorStoreService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Set up mock return value
            mock_chunks = [
                {
                    'text': 'This is about machine learning algorithms.',
                    'metadata': {'document_id': str(test_document_id), 'chunk_index': 0},
                    'distance': 0.1
                }
            ]
            mock_service.query_chunks.return_value = mock_chunks
            
            # Call the function
            query = "machine learning"
            results = query_vector_store(query, test_document_id, n_results=3)
            
            # Verify results
            assert len(results) == 1
            assert results[0]['text'] == 'This is about machine learning algorithms.'
            assert results[0]['metadata']['document_id'] == str(test_document_id)
            assert results[0]['distance'] == 0.1
            
            # Verify the mock was called correctly
            mock_service.query_chunks.assert_called_once_with(
                query_text=query,
                document_id=test_document_id,
                n_results=3
            )

    def test_query_vector_store_document_filtering(self):
        """Test that queries are properly filtered by document ID."""
        test_document_id = uuid4()
        
        with patch('app.services.vector_query_service.VectorStoreService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Mock return value - only chunks from the test document
            mock_chunks = [
                {
                    'text': 'Content from test document',
                    'metadata': {'document_id': str(test_document_id), 'chunk_index': 0},
                    'distance': 0.1
                }
            ]
            mock_service.query_chunks.return_value = mock_chunks
            
            query = "any content"
            results = query_vector_store(query, test_document_id, n_results=10)
            
            # All results should belong to the test document
            for result in results:
                assert result['metadata']['document_id'] == str(test_document_id)

    def test_query_vector_store_n_results_parameter(self):
        """Test that n_results parameter is passed correctly."""
        test_document_id = uuid4()
        
        with patch('app.services.vector_query_service.VectorStoreService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Test different n_results values
            mock_service.query_chunks.return_value = []
            
            query = "test query"
            query_vector_store(query, test_document_id, n_results=5)
            
            # Verify the service was called with correct n_results
            mock_service.query_chunks.assert_called_with(
                query_text=query,
                document_id=test_document_id,
                n_results=5
            )

    def test_query_vector_store_empty_results(self):
        """Test querying for a document that doesn't exist."""
        nonexistent_document_id = uuid4()
        
        with patch('app.services.vector_query_service.VectorStoreService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            
            # Mock empty results for non-existent document
            mock_service.query_chunks.return_value = []
            
            results = query_vector_store("any query", nonexistent_document_id)
            
            # Should return empty list for non-existent document
            assert isinstance(results, list)
            assert len(results) == 0

    def test_query_vector_store_default_parameters(self):
        """Test that the function works with default parameters."""
        test_document_id = uuid4()
        
        with patch('app.services.vector_query_service.VectorStoreService') as mock_service_class:
            mock_service = Mock()
            mock_service_class.return_value = mock_service
            mock_service.query_chunks.return_value = []
            
            # Call without specifying n_results (should default to 5)
            query_vector_store("test query", test_document_id)
            
            # Verify default n_results=5 was used
            mock_service.query_chunks.assert_called_with(
                query_text="test query",
                document_id=test_document_id,
                n_results=5
            ) 