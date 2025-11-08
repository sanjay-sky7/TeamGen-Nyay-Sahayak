import os, json
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from tqdm import tqdm

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "legal_knowledge")
OUT_DIR = os.path.join(os.path.dirname(__file__), "index")
os.makedirs(OUT_DIR, exist_ok=True)

EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE_WORDS = 450
CHUNK_OVERLAP = 80

def read_doc(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = words[i:i+CHUNK_SIZE_WORDS]
        chunks.append(" ".join(chunk))
        i += CHUNK_SIZE_WORDS - CHUNK_OVERLAP
    return chunks

def main():
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        sample_path = os.path.join(DATA_DIR, "sample_template.txt")
        if not os.path.exists(sample_path):
            with open(sample_path, "w", encoding="utf-8") as sf:
                sf.write("""source_name: sample_crime
url: https://example.com/sample_crime
date_published: 2025-01-01
jurisdiction: national
doc_type: guide

Title: Sample Crime Guide

Write a short verified 'Initial Action Roadmap' here for a specific crime.
Include steps like immediate actions, how to file FIR, evidence to preserve, and likely IPC sections.
""")
        print("Created DATA folder and sample file. Add real legal docs then rerun.")
        return

    try:
        model = SentenceTransformer(EMBED_MODEL)
    except Exception as e:
        print("Failed to load model:", e)
        return

    docs = []
    for fname in os.listdir(DATA_DIR):
        if not fname.lower().endswith((".txt", ".md")): continue
        path = os.path.join(DATA_DIR, fname)
        text = read_doc(path)
        # Support additional metadata fields: city and incident_type
        meta = {"source_name": fname, "url": "", "date_published": "", "jurisdiction": "", "doc_type": "", "city": "", "incident_type": ""}
        for ln in text.splitlines()[:10]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                if k.strip().lower() in meta:
                    meta[k.strip().lower()] = v.strip()
        chunks = chunk_text(text)
        for i, c in enumerate(chunks):
            docs.append({"id": f"{fname}__chunk{i}", "text": c, "meta": meta})

    if not docs:
        print("No valid docs found in", DATA_DIR); return

    texts = [d["text"] for d in docs]
    embeds = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    dim = embeds.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeds)
    index.add(embeds)
    faiss.write_index(index, os.path.join(OUT_DIR, "faiss_index.faiss"))
    with open(os.path.join(OUT_DIR, "metadata.jsonl"), "w", encoding="utf-8") as f:
        for d in docs:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print("Index built:", len(docs))

if __name__ == "__main__":
    main()

