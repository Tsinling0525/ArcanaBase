import os, time
from typing import List, Tuple
from loader import load_pdf, load_txt, load_md, load_url, simple_split
from rag import ingest_text_blocks, load_sources, save_sources

SUPPORTED_EXT = {".pdf": load_pdf, ".txt": load_txt, ".md": load_md}


def ingest_file(path: str, source_id: str | None = None) -> Tuple[str, int]:
    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_EXT:
        raise ValueError(f"Unsupported file type: {ext}")
    loader = SUPPORTED_EXT[ext]
    raw = loader(path)
    chunks = simple_split(raw)
    blocks = [(c, {"path": path, "offset": i}) for i, c in enumerate(chunks)]
    sid = source_id or os.path.basename(path)
    n = ingest_text_blocks(blocks, sid)
    # update sources registry
    sources = load_sources()
    sources[sid] = {"kind": "file", "title": os.path.basename(path), "meta": {"ext": ext, "mtime": time.time()}}
    save_sources(sources)
    return sid, n


def ingest_from_url(url: str, source_id: str | None = None) -> Tuple[str, int]:
    raw = load_url(url)
    chunks = simple_split(raw)
    blocks = [(c, {"url": url, "offset": i}) for i, c in enumerate(chunks)]
    sid = source_id or url
    n = ingest_text_blocks(blocks, sid)
    sources = load_sources()
    sources[sid] = {"kind": "url", "title": url, "meta": {}}
    save_sources(sources)
    return sid, n