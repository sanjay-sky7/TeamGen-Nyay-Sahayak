"""
Configuration management for Nyay Sahayak backend.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "legal_knowledge")
INDEX_DIR = os.path.join(BASE_DIR, "index")
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "faiss_index.faiss")
METADATA_PATH = os.path.join(INDEX_DIR, "metadata.jsonl")

# API Configuration
GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = "gemini-1.5-pro"  # Can be changed to "gemini-1.5-flash" for faster responses

# Embedding Configuration
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE_WORDS = 450
CHUNK_OVERLAP = 80

# RAG Configuration
TOP_K_RETRIEVAL = 3  # Number of chunks to retrieve from FAISS

# Application Settings
APP_NAME = "Nyay Sahayak API"
APP_VERSION = "1.0.0"
API_PREFIX = "/api/v1"

# Email Configuration
SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
EMAIL_FROM: Optional[str] = os.getenv("EMAIL_FROM", SMTP_USERNAME)
EMAIL_FROM_NAME: str = os.getenv("EMAIL_FROM_NAME", "Nyay Sahayak")

def validate_config():
    """
    Validate that required configuration is present.
    Raises ValueError if critical config is missing.
    """
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY environment variable is not set. "
            "Please set it in your .env file or export it."
        )
    
    # Ensure directories exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(INDEX_DIR, exist_ok=True)

