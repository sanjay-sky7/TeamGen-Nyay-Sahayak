"""
RAG Pipeline Service
Handles FAISS index loading and similarity search for document retrieval.
"""

import os
import json
import numpy as np
import faiss
from typing import List, Dict, Tuple, Optional
from sentence_transformers import SentenceTransformer
from app.config import (
    FAISS_INDEX_PATH,
    METADATA_PATH,
    EMBED_MODEL,
    TOP_K_RETRIEVAL,
    INDEX_DIR
)


class RAGPipeline:
    """
    RAG Pipeline for retrieving relevant legal documents using FAISS.
    """
    
    def __init__(self):
        """
        Initialize the RAG pipeline.
        Loads FAISS index, metadata, and embedding model.
        """
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict] = []
        self.embedding_model: Optional[SentenceTransformer] = None
        self._load_index()
    
    def _load_index(self):
        """
        Load FAISS index and metadata from disk.
        Raises FileNotFoundError if index files don't exist.
        """
        if not os.path.exists(FAISS_INDEX_PATH):
            raise FileNotFoundError(
                f"FAISS index not found at {FAISS_INDEX_PATH}. "
                "Please run build_index.py first to create the index."
            )
        
        if not os.path.exists(METADATA_PATH):
            raise FileNotFoundError(
                f"Metadata file not found at {METADATA_PATH}. "
                "Please run build_index.py first to create the metadata."
            )
        
        # Load FAISS index
        self.index = faiss.read_index(FAISS_INDEX_PATH)
        
        # Load metadata
        self.metadata = []
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    self.metadata.append(json.loads(line))
        
        # Load embedding model
        try:
            self.embedding_model = SentenceTransformer(EMBED_MODEL)
        except Exception as e:
            raise RuntimeError(f"Failed to load embedding model: {e}")
        
        print(f"RAG Pipeline loaded: {len(self.metadata)} chunks, index dimension: {self.index.d}")
    
    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL, city: Optional[str] = None, incident_type: Optional[str] = None) -> List[Dict]:
        """
        Retrieve top-k most relevant document chunks for a given query.
        
        Args:
            query: User's query text
            top_k: Number of chunks to retrieve (default: TOP_K_RETRIEVAL)
        
        Returns:
            List of dictionaries containing retrieved chunks with their metadata
        """
        if self.index is None or self.embedding_model is None:
            raise RuntimeError("RAG Pipeline not properly initialized")
        
        # Encode query
        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            show_progress_bar=False
        )
        
        # Normalize for cosine similarity (IndexFlatIP requires normalized vectors)
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding, min(top_k, len(self.metadata)))
        
        # Retrieve corresponding chunks and metadata, applying optional metadata filters
        results = []

        def matches_filters(meta: Dict) -> bool:
            if city:
                meta_city = str(meta.get("city", "") or "").strip().lower()
                if city.strip().lower() not in meta_city and meta_city not in city.strip().lower():
                    return False
            if incident_type:
                meta_inc = str(meta.get("incident_type", "") or "").strip().lower()
                if incident_type.strip().lower() not in meta_inc and meta_inc not in incident_type.strip().lower():
                    return False
            return True

        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                meta = self.metadata[idx]
                if not matches_filters(meta):
                    # skip this chunk, doesn't match provided metadata filters
                    continue
                chunk_data = meta.copy()
                # include text field if present in metadata (some workflows store text separately)
                # original builder stores text in metadata entries under 'text'
                if "text" in self.metadata[idx]:
                    chunk_data["text"] = self.metadata[idx].get("text", "")
                chunk_data["similarity_score"] = float(dist)
                results.append(chunk_data)
                if len(results) >= top_k:
                    break

        return results
    
    def is_loaded(self) -> bool:
        """
        Check if the RAG pipeline is properly loaded.
        
        Returns:
            True if index and model are loaded, False otherwise
        """
        return (
            self.index is not None and
            self.embedding_model is not None and
            len(self.metadata) > 0
        )


# Global RAG pipeline instance (singleton pattern)
_rag_pipeline: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    """
    Get or create the global RAG pipeline instance.
    
    Returns:
        RAGPipeline instance
    """
    global _rag_pipeline
    if _rag_pipeline is None:
        _rag_pipeline = RAGPipeline()
    return _rag_pipeline


def reload_rag_pipeline():
    """
    Reload the RAG pipeline (useful after rebuilding index).
    """
    global _rag_pipeline
    _rag_pipeline = RAGPipeline()

