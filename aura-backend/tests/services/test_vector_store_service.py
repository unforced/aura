import pytest
from app.services.vector_store_service import vector_store_service

def test_chromadb_connection():
    """
    Tests that the application can successfully connect to the ChromaDB server.
    """
    # The heartbeat method raises an exception if it can't connect.
    try:
        heartbeat = vector_store_service.heartbeat()
        # The heartbeat is a Unix timestamp in nanoseconds.
        # We just need to make sure it's a positive number.
        assert isinstance(heartbeat, int)
        assert heartbeat > 0
    except Exception as e:
        pytest.fail(f"ChromaDB connection test failed: {e}")

def test_get_or_create_collection():
    """
    Tests that a collection can be created in ChromaDB.
    """
    collection_name = "test-collection"
    try:
        collection = vector_store_service.get_or_create_collection(name=collection_name)
        assert collection is not None
        assert collection.name == collection_name

        # Clean up: delete the collection
        vector_store_service.client.delete_collection(name=collection_name)
    except Exception as e:
        pytest.fail(f"Failed to create or get collection '{collection_name}': {e}")

def test_add_and_query_texts():
    """
    Tests that texts can be added to and queried from a collection.
    """
    collection_name = "test-add-query"
    
    # 1. Add texts
    texts_to_add = ["The sky is blue.", "The grass is green."]
    metadatas = [{"source": "nature-facts"}, {"source": "nature-facts"}]
    ids = ["doc1", "doc2"]
    
    try:
        vector_store_service.add_texts(
            collection_name=collection_name,
            texts=texts_to_add,
            metadatas=metadatas,
            ids=ids
        )

        # 2. Query for one of the texts
        query_result = vector_store_service.query_texts(
            collection_name=collection_name,
            query_texts=["What color is the sky?"],
            n_results=1
        )

        # 3. Assert the result
        assert query_result is not None
        assert len(query_result["ids"][0]) == 1
        assert query_result["ids"][0][0] == "doc1"
        assert query_result["documents"][0][0] == "The sky is blue."

    except Exception as e:
        pytest.fail(f"Test for add/query failed: {e}")
    finally:
        # 4. Clean up
        try:
            vector_store_service.client.delete_collection(name=collection_name)
        except Exception:
            # collection might not exist if test failed early
            pass 