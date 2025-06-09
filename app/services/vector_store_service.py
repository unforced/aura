import chromadb
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