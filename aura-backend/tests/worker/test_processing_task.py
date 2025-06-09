import pytest
from uuid import uuid4
from app.crud import crud_document
from app.schemas.document_schemas import DocumentCreate
from app.worker import process_document_for_mvp
from app.services import vector_store_service
from app.db.graph_db import GraphDB
from app.core.config import settings
from app.db.session import get_db as get_test_db_session

@pytest.mark.skip(reason="Celery integration testing is complex and will be addressed later.")
def test_full_document_processing_pipeline(session, sample_pdf_path, authenticated_client):
    """
    Integration test for the full document processing pipeline.
    Uses the authenticated_client fixture to get a user and token.
    """
    # 1. Setup: The authenticated_client fixture gives us a user.
    # We just need to get their ID from the /users/me endpoint.
    response = authenticated_client.get("/api/v1/users/me")
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Create a document record for this user
    doc_in = DocumentCreate(file_name="sample.pdf", file_path=sample_pdf_path)
    document = crud_document.create_document(session, document_in=doc_in, owner_id=user_id)
    session.commit()

    # 2. Execute the Celery task (will run synchronously due to test settings)
    task_result = process_document_for_mvp.delay(str(document.id))

    assert task_result.successful(), "Celery task failed"
    assert task_result.result["status"] == "completed"

    # 3. Verification
    session = next(get_test_db_session())
    updated_doc = crud_document.get_document(session, document_id=document.id)
    assert updated_doc.status == "COMPLETED"
    session.close()

    # B. Verify Neo4j nodes and relationships
    graph_db = GraphDB(uri=settings.NEO4J_URI, user=settings.NEO4J_USER, password=settings.NEO4J_PASSWORD)
    graph_session = graph_db.get_session()
    
    doc_nodes = graph_session.run("MATCH (d:Document {id: $id}) RETURN d", id=str(document.id))
    assert doc_nodes.single() is not None
    
    chunk_nodes_result = graph_session.run("MATCH (d:Document {id: $id})-[:HAS_CHUNK]->(c:Chunk) RETURN c", id=str(document.id))
    chunk_count = len(list(chunk_nodes_result))
    assert chunk_count > 0
    
    graph_session.close()
    graph_db.close()

    # C. Verify ChromaDB embeddings
    collection_name = str(user_id)
    collection = vector_store_service.client.get_collection(name=collection_name)
    assert collection.count() == chunk_count
    
    # Clean up
    vector_store_service.client.delete_collection(name=collection_name) 