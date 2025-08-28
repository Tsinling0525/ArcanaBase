import os, re, io, requests
from bs4 import BeautifulSoup
from pypdf import PdfReader


def clean_text(t: str) -> str:
    t = t.replace("\r", " ").replace("\n", "\n").strip()
    # collapse excessive whitespace
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t


# --- file loaders ---


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return clean_text("\n\n".join(texts))


def load_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return clean_text(f.read())


# very light md loader (treat as text)
load_md = load_txt


# --- url loader ---


def load_url(url: str) -> str:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")
    # Remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title = (soup.title.string or url) if soup.title else url
    text = clean_text(soup.get_text("\n"))
    return f"{title}\n\n{text}"


# --- simple splitter ---


def simple_split(text: str, max_chars: int = 900, overlap: int = 150):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        if end == n:
            break
        start = max(0, end - overlap)
    return chunks

# --- loader registry ---


def load_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()