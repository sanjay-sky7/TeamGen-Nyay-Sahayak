"""
Nyay Sahayak Backend - Main Application Entry Point
FastAPI application for AI-powered legal assistance.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME, APP_VERSION, validate_config
from app.routes import ai_routes

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered legal assistant for Indian citizens - Your guide for legal first steps",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_routes.router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Validate configuration on startup.
    """
    try:
        validate_config()
        print(f"{APP_NAME} v{APP_VERSION} started successfully")
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set GOOGLE_API_KEY environment variable")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

