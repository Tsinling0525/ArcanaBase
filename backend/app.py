import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv
from models import QueryRequest, QueryResponse
from rag import search, synthesize_answer, load_sources
from ingest import ingest_file, ingest_from_url

load_dotenv()
app = FastAPI(title="NotebookLM‑Style RAG KB")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/sources")
def sources():
    return load_sources()

@app.post("/ingest/file")
async def ingest_file_endpoint(file: UploadFile = File(...), source_id: str = Form(None)):
    # save to temp then ingest
    os.makedirs("/tmp/rag_uploads", exist_ok=True)
    tmp_path = os.path.join("/tmp/rag_uploads", file.filename)
    with open(tmp_path, "wb") as f:
        f.write(await file.read())
    sid, n = ingest_file(tmp_path, source_id)
    return {"source_id": sid, "chunks": n}

@app.post("/ingest/url")
async def ingest_url_endpoint(payload: dict):
    url = payload.get("url")
    source_id = payload.get("source_id")
    sid, n = ingest_from_url(url, source_id)
    return {"source_id": sid, "chunks": n}

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    hits = search(req.question, top_k=req.top_k)
    answer = synthesize_answer(req.question, hits, persona=req.persona, llm=req.llm)
    return {
        "answer": answer,
        "hits": [h.model_dump() for h in hits]
    }

# run: uvicorn app:app --reload --port 8000