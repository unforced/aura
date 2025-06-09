from celery.utils.log import get_task_logger
from uuid import UUID
from sqlmodel import Session

from app.core.celery_app import celery_app
from app.db.session import engine
from app.crud import crud_document
from app.services import (
    process_document,
    graph_service,
    vector_store_service,
)


logger = get_task_logger(__name__)


@celery_app.task
def process_document_for_mvp(document_id_str: str):
    """
    The main Celery task to process a document for the MVP.
    """
    doc_id = UUID(document_id_str)
    logger.info(f"Starting processing for document {doc_id}")

    with Session(engine) as session:
        try:
            document = crud_document.get_document(session, document_id=doc_id)
            if not document:
                logger.error(f"Document with ID {doc_id} not found.")
                return

            crud_document.update_document_status(session, document=document, status="PROCESSING")

            text_chunks = process_document(document.file_path)

            # Create IDs and metadata for each chunk
            chunk_ids = [f"{doc_id}_{i}" for i in range(len(text_chunks))]
            metadatas = [{"document_id": str(doc_id), "chunk_index": i} for i in range(len(text_chunks))]

            vector_store_service.add_texts(
                collection_name="documents",
                texts=text_chunks,
                ids=chunk_ids,
                metadatas=metadatas
            )
            
            graph_service.create_document_graph(session, document)

            crud_document.update_document_status(session, document=document, status="COMPLETED")
            logger.info(f"Successfully processed document: {doc_id}")

        except Exception as e:
            logger.error(f"Error processing document {doc_id}: {e}", exc_info=True)
            with Session(engine) as final_session:
                doc_to_fail = crud_document.get_document(final_session, document_id=doc_id)
                if doc_to_fail:
                    crud_document.update_document_status(final_session, document=doc_to_fail, status="FAILED")
            raise 