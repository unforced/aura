from celery import Celery
from uuid import UUID
from pypdf import PdfReader

from app.core.config import get_settings
from app.db.session import get_db as get_pg_session
from app.db.graph_db import GraphDB
from app.crud import crud_document
from app.services import (
    document_processing_service,
    embedding_service,
    graph_service,
    vector_store_service,
)
from sqlmodel import SQLModel

# Use the same settings logic as the main app
settings = get_settings()

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url
)

# Apply settings from the config module
celery_app.conf.update(
    task_always_eager=settings.TESTING,
    task_track_started=not settings.TESTING,
)

@celery_app.task
def add(x, y):
    return x + y

@celery_app.task(bind=True)
def process_document_for_mvp(self, document_id_pg: str):
    """
    Celery task to process a document for the MVP.
    """
    pg_session_gen = get_pg_session()
    pg_db = next(pg_session_gen)
    
    graph_db = GraphDB(
        uri=settings.NEO4J_URI,
        user=settings.NEO4J_USER,
        password=settings.NEO4J_PASSWORD,
    )
    graph_session = graph_db.get_session()

    document = None
    try:
        doc_id = UUID(document_id_pg)
        document = crud_document.get_document(pg_db, document_id=doc_id)
        if not document:
            print(f"Error: Document with ID {document_id_pg} not found.")
            return {"status": "failed", "error": "Document not found"}

        crud_document.update_document_status(pg_db, document=document, status="PROCESSING")

        # 1. Parse PDF
        reader = PdfReader(document.file_path)
        full_text = "".join(page.extract_text() for page in reader.pages)

        # 2. Chunk text
        chunks = document_processing_service.chunk_text(full_text)

        # 3. Create Document node in Neo4j
        graph_service.save_document_node(graph_session, document_id=document.id)

        # 4. Process each chunk
        chunk_texts = []
        chunk_nodes = []
        for text in chunks:
            chunk_node = graph_service.ChunkNode(text=text, document_id=document.id)
            graph_service.save_chunk(graph_session, chunk=chunk_node)
            chunk_texts.append(text)
            chunk_nodes.append(chunk_node)

        # 5. Embed and store in vector DB
        embeddings = embedding_service.embed_texts(chunk_texts)
        vector_store_service.add_texts(
            collection_name=str(document.owner_id),
            texts=chunk_texts,
            metadatas=[{"document_id": str(document.id), "chunk_id": str(cn.id)} for cn in chunk_nodes],
            ids=[str(cn.id) for cn in chunk_nodes]
        )
        
        crud_document.update_document_status(pg_db, document=document, status="COMPLETED")
        print(f"Finished processing document: {document_id_pg}")
        return {"document_id": document_id_pg, "status": "completed"}

    except Exception as e:
        print(f"Error processing document {document_id_pg}: {e}")
        if document:
            crud_document.update_document_status(pg_db, document=document, status="FAILED")
        raise
    finally:
        graph_session.close()
        # pg_db is closed by the 'with' context in get_db 