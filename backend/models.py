from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class IngestURL(BaseModel):
    url: str
    source_id: Optional[str] = None # optional custom id


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    persona: Optional[str] = None # e.g., "diviner" for fortune‑telling tone later
    llm: Optional[str] = None # e.g., "gemini"


class Chunk(BaseModel):
    id: str
    source_id: str
    text: str
    metadata: Dict[str, Any]
    vector_index: Optional[int] = None


class Source(BaseModel):
    source_id: str
    kind: str # file|url
    title: str
    meta: Dict[str, Any] = {}


class QueryHit(BaseModel):
    score: float
    chunk: Chunk


class QueryResponse(BaseModel):
    answer: str
    hits: List[QueryHit]