import os, json, uuid, faiss, numpy as np
from typing import Dict, List, Tuple
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from models import Chunk, QueryHit
import google.generativeai as genai

load_dotenv()
STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
USE_GEMINI = os.getenv("USE_GEMINI", "false").lower() == "true"

if USE_GEMINI:
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is not set")
    genai.configure(api_key=gemini_key)


os.makedirs(STORAGE_DIR, exist_ok=True)
INDEX_PATH = os.path.join(STORAGE_DIR, "index.faiss")
CHUNKS_PATH = os.path.join(STORAGE_DIR, "chunks.jsonl")
SOURCES_PATH = os.path.join(STORAGE_DIR, "sources.json")

# lazy singletons
_model = None
_index = None
_dim = None

# --- Embeddings ---

def get_model():
    global _model, _dim
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
        _dim = _model.get_sentence_embedding_dimension()
    return _model

# --- Storage helpers ---

def load_index() -> faiss.IndexFlatIP:
    global _index
    if _index is not None:
        return _index
    model = get_model()
    dim = model.get_sentence_embedding_dimension()
    if os.path.exists(INDEX_PATH):
        _index = faiss.read_index(INDEX_PATH)
    else:
        _index = faiss.IndexFlatIP(dim)
    return _index


def save_index():
    if _index is not None:
        faiss.write_index(_index, INDEX_PATH)


def append_chunk_record(chunk: Chunk):
    with open(CHUNKS_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(chunk.model_dump()) + "\n")


def load_all_chunks() -> List[Chunk]:
    chunks: List[Chunk] = []
    if not os.path.exists(CHUNKS_PATH):
        return chunks
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            chunks.append(Chunk(**obj))
    return chunks


def load_sources() -> Dict[str, dict]:
    if os.path.exists(SOURCES_PATH):
        with open(SOURCES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sources(sources: Dict[str, dict]):
    with open(SOURCES_PATH, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)

# --- Ingest ---

def embed_texts(texts: List[str]) -> np.ndarray:
    model = get_model()
    emb = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return emb.astype("float32")


def ingest_text_blocks(blocks: List[Tuple[str, dict]], source_id: str) -> int:
    """
    blocks: list of (text, metadata) for a single source
    returns: number of chunks added
    """
    index = load_index()
    added = 0
    for text, metadata in blocks:
        vec = embed_texts([text])
        start_id = index.ntotal
        index.add(vec)
        chunk = Chunk(
            id=str(uuid.uuid4()),
            source_id=source_id,
            text=text,
            metadata=metadata,
            vector_index=start_id,
        )
        append_chunk_record(chunk)
        added += 1
    save_index()
    return added

# --- Query ---

def search(question: str, top_k: int = 5) -> List[QueryHit]:
    index = load_index()
    if index.ntotal == 0:
        return []
    qvec = embed_texts([question])
    scores, idxs = index.search(qvec, top_k)
    idxs = idxs[0]
    scores = scores[0]
    # Build map from vector_index -> chunk
    all_chunks = load_all_chunks()
    by_vec = {c.vector_index: c for c in all_chunks if c.vector_index is not None}
    hits: List[QueryHit] = []
    for i, score in zip(idxs, scores):
        if i == -1: # FAISS returns -1 when not enough results
            continue
        c = by_vec.get(int(i))
        if c:
            hits.append(QueryHit(score=float(score), chunk=c))
    return hits

# --- Answer synthesis ---

def synthesize_answer(
    question: str, hits: List[QueryHit], persona: str | None = None, llm: str | None = None
) -> str:
    if not hits:
        return "暂时没有足够的知识匹配到你的问题。请先导入一些资料再试试。"

    if llm == "gemini" and USE_GEMINI:
        return synthesize_answer_gemini(question, hits, persona)

    # Extractive fallback: pick 2-3 best snippets
    snippets = [h.chunk.text.strip().replace("\n", " ") for h in hits[:3]]
    base = "\n\n".join(f"• {s[:400]}..." for s in snippets)
    if persona == "diviner":
        return (
            f"【知库解读】基于已导入资料，我看到这些关键信息与你的问题有关：\n{base}\n\n"
            "这只是根据知识库检索到的线索做的理性总结，不构成命理建议🙂。"
        )
    return f"基于知识库检索，与你的问题最相关的要点：\n{base}"


def synthesize_answer_gemini(question: str, hits: List[QueryHit], persona: str | None = None) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    context = "\n\n".join([h.chunk.text for h in hits])
    prompt = f"""你是一个知识库助手。请根据以下背景信息来回答问题。
背景信息:
---
{context}
---
问题: {question}
"""
    if persona:
        prompt += f"\n请用 {persona} 的身份口吻来回答。"

    resp = model.generate_content(prompt)
    return resp.text
