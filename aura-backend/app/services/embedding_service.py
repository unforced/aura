from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the embedding service by loading the sentence-transformer model.
        """
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Creates embeddings for a list of texts.

        Args:
            texts: A list of strings to be embedded.

        Returns:
            A list of embeddings, where each embedding is a list of floats.
        """
        embeddings = self.model.encode(texts)
        # Convert numpy arrays to lists of floats
        return [embedding.tolist() for embedding in embeddings]

# Create a single, shared instance of the service
embedding_service = EmbeddingService() 