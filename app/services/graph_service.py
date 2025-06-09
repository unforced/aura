from uuid import UUID
from sqlmodel import Session
from app.db.models_pg import Document
from app.db.graph_db import GraphDB
from app.core.config import settings

class GraphService:
    """
    Service for interacting with the Neo4j graph database.
    """
    def __init__(self, graph_db: GraphDB):
        self.db = graph_db

    def create_document_graph(self, document: Document):
        """
        Creates a basic graph representation for a document.
        For the MVP, this just creates a single Document node.
        """
        with self.db.get_session() as graph_session:
            # Create the parent document node
            query = "MERGE (d:Document {id: $id, name: $name})"
            graph_session.run(query, id=str(document.id), name=document.file_name)
            print(f"Graph representation for document {document.id} created.")


def get_graph_service() -> GraphService:
    """
    Dependency to get the graph service.
    """
    graph_db = GraphDB(
        uri=settings.NEO4J_URI,
        user=settings.NEO4J_USER,
        password=settings.NEO4J_PASSWORD,
    )
    return GraphService(graph_db) 