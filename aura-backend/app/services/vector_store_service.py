import chromadb
from typing import List, Dict, Any
from uuid import UUID
from app.core.config import settings

class VectorStoreService:
    def __init__(self, host: str, port: int):
        # For testing, we might use an in-memory ephemeral client
        if settings.TESTING:
            self.client = chromadb.EphemeralClient()
        else:
            self.client = chromadb.HttpClient(host=host, port=port)
        
        # This is temporary until we have a proper collection management system
        self.collection = self.client.get_or_create_collection("aura_collection")

    def add_texts(self, ids: list[str], documents: list[str], metadatas: list[dict]):
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def query_chunks(self, query_text: str, document_id: UUID, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the vector store for the most relevant text chunks for a given document.
        
        Args:
            query_text: The text to search for
            document_id: UUID of the document to search within
            n_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing chunk data with keys: 'text', 'metadata', 'distance'
        """
        # Query the collection, filtering by document_id
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"document_id": str(document_id)}
        )
        
        # Format the results into a more usable structure
        chunks = []
        if results and results['documents'] and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0] if results['metadatas'] else [{}] * len(documents)
            distances = results['distances'][0] if results['distances'] else [0.0] * len(documents)
            
            for i, doc in enumerate(documents):
                chunks.append({
                    'text': doc,
                    'metadata': metadatas[i] if i < len(metadatas) else {},
                    'distance': distances[i] if i < len(distances) else 0.0
                })
        
        return chunks

    def heartbeat(self):
        """Returns the server's heartbeat."""
        return self.client.heartbeat() 