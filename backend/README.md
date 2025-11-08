# Nyay Sahayak Backend

**Your AI Guide for Legal First Steps**

Nyay Sahayak is an AI-powered legal assistant that helps Indian citizens understand the first legal steps after a crime or incident. Users describe what happened in plain language, and the AI replies with a structured "Initial Action Roadmap" containing immediate actions, FIR steps, evidence to preserve, and relevant IPC/IT Act sections.

## 🎯 Features

- **AI-Powered Legal Guidance**: Uses Google Gemini 1.5 Pro for intelligent legal advice
- **RAG Pipeline**: Retrieval-Augmented Generation using FAISS vector database
- **Structured Responses**: Returns JSON with crime type, actions, FIR steps, evidence, and relevant laws
- **FastAPI Backend**: Modern, async Python backend with automatic API documentation

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **LLM**: Google Gemini 1.5 Pro
- **Embeddings**: all-MiniLM-L6-v2 (SentenceTransformers)
- **Vector DB**: FAISS (local)
- **Data Storage**: `/data/legal_knowledge/` directory

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- Google API Key for Gemini (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Setup Steps

1. **Clone or navigate to the project directory**

```bash
cd nyay_sahayak_backend
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here

# Email Configuration (for sending FIR drafts)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
EMAIL_FROM_NAME=Nyay Sahayak
```

**Note for Gmail users:**
- You need to use an "App Password" instead of your regular password
- Enable 2-Step Verification on your Google account
- Generate an App Password: https://myaccount.google.com/apppasswords
- Use the 16-character app password in `SMTP_PASSWORD`

Or export it directly:

```bash
# On Windows (PowerShell)
$env:GOOGLE_API_KEY="your_google_api_key_here"

# On Linux/Mac
export GOOGLE_API_KEY="your_google_api_key_here"
```

5. **Add legal knowledge documents**

Place your legal knowledge files (`.txt` or `.md`) in the `data/legal_knowledge/` directory. Each file should follow this format:

```
source_name: ipc_sections
url: https://example.com/ipc
date_published: 2025-01-01
jurisdiction: national
doc_type: guide

Title: IPC Sections Guide

Your legal content here...
```

6. **Build the knowledge index**

```bash
python build_index.py
```

This will:
- Read all `.txt` and `.md` files from `data/legal_knowledge/`
- Chunk the documents (450 words per chunk, 80 word overlap)
- Generate embeddings using SentenceTransformers
- Build a FAISS index and save metadata

7. **Run the API server**

```bash
uvicorn main:app --reload
```

Or use Python directly:

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### POST `/api/v1/send-fir-email`

Process a user query, generate FIR draft, and send it via email.

**Request Body:**
```json
{
  "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP.",
  "email": "user@example.com",
  "user_name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "message": "FIR draft sent successfully to your email",
  "email_sent_to": "user@example.com"
}
```

### POST `/api/v1/query`

Process a user query and return a structured legal roadmap.

**Request Body:**
```json
{
  "query": "I was scammed online. Someone called me pretending to be from my bank and took my OTP."
}
```

**Response:**
```json
{
  "crime_type": "Cyber Fraud",
  "immediate_actions": [
    "Block your debit/credit card immediately",
    "Report to your bank's fraud helpline"
  ],
  "fir_steps": [
    "Visit nearest cyber police station",
    "File e-FIR at https://cybercrime.gov.in"
  ],
  "evidence_to_preserve": [
    "Screenshots of chats",
    "Transaction receipts",
    "Call recordings"
  ],
  "relevant_laws": [
    "IPC 420 – Cheating",
    "IT Act 66D – Impersonation"
  ]
}
```

### POST `/api/v1/ingest`

Rebuild the FAISS index from legal knowledge documents.

**Response:**
```json
{
  "message": "Index rebuilt successfully",
  "documents_processed": 10,
  "chunks_created": 10
}
```

### GET `/api/v1/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "index_loaded": true,
  "gemini_configured": true
}
```

## 📁 Project Structure

```
nyay_sahayak_backend/
├── main.py                 # FastAPI app entry point
├── build_index.py          # Embedding script for building FAISS index
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── models/
│   │   └── schemas.py      # Pydantic models
│   ├── routes/
│   │   └── ai_routes.py    # API endpoints
│   ├── services/
│   │   ├── rag_pipeline.py    # FAISS retrieval logic
│   │   └── query_handler.py   # Gemini API wrapper
│   └── utils/
│       └── __init__.py
├── index/
│   ├── faiss_index.faiss  # FAISS index file (generated)
│   └── metadata.jsonl     # Document metadata (generated)
├── data/
│   └── legal_knowledge/    # Place your legal documents here
│       ├── ipc_sections.txt
│       ├── fir_process.txt
│       └── cybercrime.txt
├── requirements.txt
├── README.md
└── .env                    # Environment variables (create this)
```

## 🔧 Configuration

Edit `app/config.py` to customize:

- `GEMINI_MODEL`: Change to `"gemini-1.5-flash"` for faster responses
- `TOP_K_RETRIEVAL`: Number of chunks to retrieve (default: 3)
- `CHUNK_SIZE_WORDS`: Document chunk size (default: 450)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 80)

## 🧪 Testing

Test the API using curl:

```bash
curl -X POST "http://localhost:8000/api/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "I was scammed online"}'
```

Or use the interactive Swagger UI at `/docs`.

## 🐛 Troubleshooting

### "FAISS index not found"
- Run `python build_index.py` to create the index
- Ensure you have legal documents in `data/legal_knowledge/`

### "GOOGLE_API_KEY is not configured"
- Set the `GOOGLE_API_KEY` environment variable
- Create a `.env` file with your API key

### "Failed to load embedding model"
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check your internet connection (first run downloads the model)

## 📝 License

This project is part of a hackathon submission for MLHack.

## 🤝 Contributing

This is a hackathon project. For improvements, please create issues or pull requests.

## 📧 Contact

For questions or issues, please refer to the hackathon documentation.

---

**Built with ❤️ for MLHack - AI for Trust & Transparency**

