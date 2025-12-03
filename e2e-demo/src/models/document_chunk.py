"""Document chunk model for vector storage.

Provides a dataclass for representing document chunks that are
stored in the vector database for semantic search.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class DocumentChunk:
    """A chunk of a document stored in the vector database.
    
    Attributes:
        chunk_id: Unique identifier for this chunk
        document_path: Path to the source document
        content: The text content of this chunk
        metadata: Additional metadata about the chunk
        embedding: Optional pre-computed embedding vector
    """
    chunk_id: str
    document_path: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert chunk to dictionary for storage."""
        return {
            "chunk_id": self.chunk_id,
            "document_path": self.document_path,
            "content": self.content,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentChunk":
        """Create a DocumentChunk from a dictionary."""
        return cls(
            chunk_id=data["chunk_id"],
            document_path=data["document_path"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            embedding=data.get("embedding")
        )
