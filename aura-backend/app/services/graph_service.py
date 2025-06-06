from neo4j import Session
from app.models.graph import ChunkNode
import uuid

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
    
    if record:
        return chunk
    
    return None # Or raise an exception 