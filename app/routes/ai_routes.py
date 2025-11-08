"""
AI Routes for Nyay Sahayak API
Defines FastAPI endpoints for query processing and index management.
"""

import os
import subprocess
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    QueryRequest,
    RoadmapResponse,
    ErrorResponse,
    HealthResponse,
    IngestResponse,
    EmailFIRRequest,
    EmailFIRResponse
)
from app.services.query_handler import QueryHandler
from app.services.rag_pipeline import get_rag_pipeline, reload_rag_pipeline
from app.services.email_service import get_email_service
from app.config import GOOGLE_API_KEY, APP_VERSION, validate_config

router = APIRouter(tags=["AI"])

# Initialize query handler (lazy loading)
_query_handler: QueryHandler = None


def get_query_handler() -> QueryHandler:
    """
    Get or create the query handler instance.
    
    Returns:
        QueryHandler instance
    """
    global _query_handler
    if _query_handler is None:
        try:
            _query_handler = QueryHandler()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to initialize query handler: {str(e)}"
            )
    return _query_handler


@router.post("/query", response_model=RoadmapResponse, status_code=status.HTTP_200_OK)
async def process_query(request: QueryRequest):
    """
    Process user query and return structured legal roadmap.
    
    Args:
        request: QueryRequest containing user's description
    
    Returns:
        RoadmapResponse with structured legal guidance
    
    Raises:
        HTTPException: If processing fails
    """
    try:
        handler = get_query_handler()
        # Pass optional city and incident_type to the query handler so
        # retrieval can be filtered by metadata when available.
        result = await handler.process_query(
            request.query,
            city=getattr(request, "city", None),
            incident_type=getattr(request, "incident_type", None)
        )
        
        return RoadmapResponse(
            crime_type=result.get("crime_type", "Legal Matter"),
            immediate_actions=result.get("immediate_actions", []),
            fir_steps=result.get("fir_steps", []),
            evidence_to_preserve=result.get("evidence_to_preserve", []),
            relevant_laws=result.get("relevant_laws", [])
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.post("/ingest", response_model=IngestResponse, status_code=status.HTTP_200_OK)
async def rebuild_index():
    """
    Rebuild the FAISS index from legal knowledge documents.
    This endpoint runs build_index.py to recreate the index.
    
    Returns:
        IngestResponse with processing statistics
    
    Raises:
        HTTPException: If index building fails
    """
    try:
        # Get the path to build_index.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        build_script = os.path.join(base_dir, "build_index.py")
        
        if not os.path.exists(build_script):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="build_index.py not found"
            )
        
        # Run build_index.py
        result = subprocess.run(
            ["python", build_script],
            capture_output=True,
            text=True,
            cwd=base_dir
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Index building failed: {result.stderr}"
            )
        
        # Reload RAG pipeline with new index
        try:
            reload_rag_pipeline()
        except Exception as e:
            # Index might not exist yet, that's okay
            print(f"Warning: Could not reload RAG pipeline: {e}")
        
        # Parse output to get document count (if available)
        output_lines = result.stdout.split("\n")
        doc_count = 0
        for line in output_lines:
            if "Index built:" in line:
                try:
                    doc_count = int(line.split(":")[-1].strip())
                except:
                    pass
        
        return IngestResponse(
            message="Index rebuilt successfully",
            documents_processed=doc_count,
            chunks_created=doc_count  # Approximate, actual chunks may vary
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error rebuilding index: {str(e)}"
        )


@router.post("/send-fir-email", response_model=EmailFIRResponse, status_code=status.HTTP_200_OK)
async def send_fir_email(request: EmailFIRRequest):
    """
    Process user query, generate FIR draft, and send it via email.
    
    Args:
        request: EmailFIRRequest containing user query and email address
    
    Returns:
        EmailFIRResponse with email sending status
    
    Raises:
        HTTPException: If processing or email sending fails
    """
    try:
        # Process the query to get roadmap
        handler = get_query_handler()
        roadmap = await handler.process_query(
            request.query,
            city=getattr(request, "city", None),
            incident_type=getattr(request, "incident_type", None)
        )
        
        # Send email with FIR draft
        email_service = get_email_service()
        email_service.send_fir_draft(
            to_email=request.email,
            roadmap=roadmap,
            user_query=request.query,
            user_name=request.user_name
        )
        
        return EmailFIRResponse(
            success=True,
            message="FIR draft sent successfully to your email",
            email_sent_to=request.email
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending FIR draft email: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        HealthResponse with service status information
    """
    try:
        # Check if RAG pipeline is loaded
        rag_pipeline = get_rag_pipeline()
        index_loaded = rag_pipeline.is_loaded()
    except Exception:
        index_loaded = False
    
    # Check if Gemini is configured
    gemini_configured = GOOGLE_API_KEY is not None and GOOGLE_API_KEY != ""
    
    return HealthResponse(
        status="healthy" if (index_loaded and gemini_configured) else "degraded",
        version=APP_VERSION,
        index_loaded=index_loaded,
        gemini_configured=gemini_configured
    )

