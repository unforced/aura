import pytest
from uuid import uuid4
from neo4j import GraphDatabase
from app.models.graph import ChunkNode
from app.services.graph_service import save_chunk
from app.core.config import settings

@pytest.fixture(scope="module")
def graph_db_driver():
    """Provides a direct Neo4j driver for the test module, bypassing app state."""
    driver = GraphDatabase.driver(
        settings.NEO4J_URI, 
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
    )
    yield driver
    driver.close()

@pytest.fixture()
def graph_session(graph_db_driver):
    """Provides a Neo4j session for a single test function."""
    session = graph_db_driver.session()
    yield session
    session.close()

def test_save_chunk(graph_session):
    """
    Tests that a ChunkNode can be successfully saved to the graph database.
    """
    # 1. Create a ChunkNode instance
    test_document_id = uuid4()
    chunk_to_save = ChunkNode(
        text="This is a test chunk.",
        document_id=test_document_id
    )

    # 2. Call save_chunk
    saved_chunk = save_chunk(graph_session, chunk_to_save)

    # 3. Verify the returned chunk
    assert saved_chunk is not None
    assert saved_chunk.id == chunk_to_save.id
    assert saved_chunk.text == "This is a test chunk."

    # 4. Query the database directly to confirm creation
    result = graph_session.run(
        "MATCH (c:Chunk {id: $id}) RETURN c.text AS text, c.document_id AS document_id",
        id=str(chunk_to_save.id)
    )
    record = result.single()
    assert record is not None
    assert record["text"] == "This is a test chunk."
    assert record["document_id"] == str(test_document_id)

    # 5. Clean up the created node
    graph_session.run("MATCH (c:Chunk {id: $id}) DELETE c", id=str(chunk_to_save.id)) 