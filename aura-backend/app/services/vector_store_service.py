import chromadb
from app.core.config import settings

class VectorStoreService:
    def __init__(self, host: str, port: int):
        self.client = chromadb.HttpClient(host=host, port=port)

    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(name)

    def add_texts(self, collection_name: str, texts: list[str], metadatas: list[dict] = None, ids: list[str] = None):
        """Adds texts to a collection."""
        collection = self.client.get_or_create_collection(name=collection_name)
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def query_texts(self, collection_name: str, query_texts: list[str], n_results: int = 5):
        """Queries a collection by text."""
        collection = self.client.get_or_create_collection(name=collection_name)
        return collection.query(
            query_texts=query_texts,
            n_results=n_results
        )

    def heartbeat(self):
        """Returns the server's heartbeat."""
        return self.client.heartbeat()

vector_store_service = VectorStoreService(
    host=settings.CHROMA_HOST,
    port=settings.CHROMA_PORT
) 