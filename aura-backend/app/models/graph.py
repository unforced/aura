from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class BaseNode(BaseModel):
    id: UUID = Field(default_factory=uuid4)

class ChunkNode(BaseNode):
    text: str
    document_id: UUID

class BaseRelationship(BaseModel):
    source: UUID
    target: UUID
    type: str

class HasChunk(BaseRelationship):
    type: str = "HAS_CHUNK" 