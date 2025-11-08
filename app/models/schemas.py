"""
Pydantic models for request/response validation.
Defines the structure of API inputs and outputs.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class QueryRequest(BaseModel):
    """
    Request model for user query endpoint.
    """
    query: str = Field(
        ...,
        description="User's description of the incident or legal situation",
        min_length=10,
        max_length=2000,
        example="I was scammed online. Someone called me pretending to be from my bank and took my OTP."
    )
    city: Optional[str] = Field(
        None,
        description="Optional city where the incident occurred",
        example="Mumbai"
    )
    incident_type: Optional[str] = Field(
        None,
        description="Optional incident type to help narrow retrieval",
        example="UPI payment fraud"
    )


class RoadmapResponse(BaseModel):
    """
    Response model for the structured legal roadmap.
    """
    crime_type: str = Field(
        ...,
        description="Identified type of crime or incident",
        example="Cyber Fraud"
    )
    immediate_actions: List[str] = Field(
        ...,
        description="List of immediate actions the user should take",
        example=[
            "Block your debit/credit card immediately",
            "Report to your bank's fraud helpline"
        ]
    )
    fir_steps: List[str] = Field(
        ...,
        description="Step-by-step process for filing an FIR",
        example=[
            "Visit nearest cyber police station",
            "File e-FIR at https://cybercrime.gov.in"
        ]
    )
    evidence_to_preserve: List[str] = Field(
        ...,
        description="List of evidence items to preserve",
        example=[
            "Screenshots of chats",
            "Transaction receipts",
            "Call recordings"
        ]
    )
    relevant_laws: List[str] = Field(
        ...,
        description="Relevant IPC/IT Act sections applicable to the case",
        example=[
            "IPC 420 – Cheating",
            "IT Act 66D – Impersonation"
        ]
    )


class ErrorResponse(BaseModel):
    """
    Error response model for API errors.
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


class HealthResponse(BaseModel):
    """
    Health check response model.
    """
    status: str = Field(..., description="Service status", example="healthy")
    version: str = Field(..., description="API version", example="1.0.0")
    index_loaded: bool = Field(..., description="Whether FAISS index is loaded")
    gemini_configured: bool = Field(..., description="Whether Gemini API is configured")


class IngestResponse(BaseModel):
    """
    Response model for index ingestion endpoint.
    """
    message: str = Field(..., description="Status message")
    documents_processed: int = Field(..., description="Number of documents processed")
    chunks_created: int = Field(..., description="Number of chunks created")


class EmailFIRRequest(BaseModel):
    """
    Request model for sending FIR draft via email.
    """
    query: str = Field(
        ...,
        description="User's description of the incident or legal situation",
        min_length=10,
        max_length=2000,
        example="I was scammed online. Someone called me pretending to be from my bank and took my OTP."
    )
    email: EmailStr = Field(
        ...,
        description="User's email address where the FIR draft will be sent",
        example="user@example.com"
    )
    user_name: Optional[str] = Field(
        None,
        description="User's name (optional)",
        example="John Doe"
    )
    city: Optional[str] = Field(
        None,
        description="Optional city where the incident occurred",
        example="Mumbai"
    )
    incident_type: Optional[str] = Field(
        None,
        description="Optional incident type to help narrow retrieval",
        example="UPI payment fraud"
    )


class EmailFIRResponse(BaseModel):
    """
    Response model for email FIR draft endpoint.
    """
    success: bool = Field(..., description="Whether the email was sent successfully")
    message: str = Field(..., description="Status message")
    email_sent_to: str = Field(..., description="Email address where the FIR draft was sent")

