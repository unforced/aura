from celery.utils.log import get_task_logger
from uuid import UUID
from sqlmodel import Session

from app.core.celery_app import celery_app
from app.db.session import engine
from app.crud import crud_document
from app.services.document_processing_service import process_document
from app.services.graph_service import GraphService
from app.services.vector_store_service import VectorStoreService
from app.db.graph_db import GraphDB
from app.core.config import settings
from app.db.models_pg import DocumentStatus


logger = get_task_logger(__name__)


@celery_app.task
def process_document_for_mvp(document_id_str: str):
    """
    The main Celery task to process a document for the MVP.
    """
    doc_id = UUID(document_id_str)
    logger.info(f"Starting processing for document {doc_id}")

    # Initialize services here, now that they don't connect on import
    graph_db = GraphDB(
        uri=settings.NEO4J_URI,
        user=settings.NEO4J_USER,
        password=settings.NEO4J_PASSWORD,
    )
    graph_service = GraphService(graph_db)
    vector_store_service = VectorStoreService(
        host=settings.CHROMA_HOST, port=settings.CHROMA_PORT
    )

    with Session(engine) as session:
        try:
            # 1. Get the document from the database
            document = crud_document.get_document(session, document_id=doc_id)
            if not document:
                logger.error(f"Document with ID {doc_id} not found.")
                return

            crud_document.update_document_status(
                session, document=document, status=DocumentStatus.PROCESSING
            )

            # 2. Parse the document to get text chunks
            text_chunks = process_document(document.file_path)

            # 3. Add text chunks to the vector store
            chunk_ids = [f"{doc_id}_{i}" for i in range(len(text_chunks))]
            vector_store_service.add_texts(
                ids=chunk_ids,
                documents=text_chunks,
                metadatas=[{"document_id": str(doc_id)}] * len(text_chunks),
            )
            logger.info(f"Added {len(text_chunks)} chunks to vector store.")

            # 4. Create a graph representation in Neo4j
            graph_service.create_document_graph(document=document)
            logger.info(f"Created graph representation for document {doc_id}.")

            # 5. Update the document status to COMPLETED
            crud_document.update_document_status(
                session, document=document, status=DocumentStatus.COMPLETED
            )
            logger.info(f"Successfully processed document {doc_id}.")

        except Exception as e:
            logger.error(f"Error processing document {doc_id}: {e}", exc_info=True)
            # Attempt to mark the document as FAILED
            document = crud_document.get_document(session, document_id=doc_id)
            if document:
                crud_document.update_document_status(
                    session, document=document, status=DocumentStatus.FAILED
                ) 