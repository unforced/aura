from neo4j import Session
from app.models.graph import ChunkNode
from uuid import UUID

def save_document_node(session: Session, document_id: UUID) -> None:
    """
    Creates or updates a Document node in the graph.
    """
    query = (
        "MERGE (d:Document {id: $id})"
        "RETURN d"
    )
    session.run(query, id=str(document_id))

def save_chunk(session: Session, chunk: ChunkNode) -> ChunkNode:
    """
    Saves a ChunkNode to the graph database.
    """
    # Using MERGE on the chunk's UUID to prevent creating duplicate nodes
    # if this operation is ever re-run with the same chunk.
    query = (
        "MERGE (c:Chunk {id: $id}) "
        "ON CREATE SET c.text = $text, c.document_id = $document_id "
        "RETURN c"
    )
    
    result = session.run(query, id=str(chunk.id), text=chunk.text, document_id=str(chunk.document_id))
    
    # We can add more robust error handling here later
    record = result.single()
    
    # After saving the chunk, link it to its parent document
    if record:
        link_chunk_to_document(session, document_id=chunk.document_id, chunk_id=chunk.id)
        return chunk
    
    return None # Or raise an exception 

def link_chunk_to_document(session: Session, document_id: UUID, chunk_id: UUID) -> None:
    """
    Creates a HAS_CHUNK relationship between a Document and a Chunk node.
    """
    query = (
        "MATCH (d:Document {id: $document_id}) "
        "MATCH (c:Chunk {id: $chunk_id}) "
        "MERGE (d)-[:HAS_CHUNK]->(c)"
    )
    session.run(query, document_id=str(document_id), chunk_id=str(chunk_id)) 