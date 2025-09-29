"""
Main FastAPI application for Full-Stack AI Apps
Provides REST API endpoints for AI services across multiple cloud platforms
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import logging
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from .services.aws_service import AWSService
from .services.gcp_service import GCPService  
from .services.azure_service import AzureService
from .mcp.server import MCPServer
from .common.config import Settings
from .common.logging import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Initialize settings
settings = Settings()

# Initialize services
aws_service = AWSService()
gcp_service = GCPService()
azure_service = AzureService()
mcp_server = MCPServer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Full-Stack AI Apps...")
    await aws_service.initialize()
    await gcp_service.initialize()
    await azure_service.initialize()
    await mcp_server.start()
    
    yield
    
    # Shutdown
    logger.info("Shutting down Full-Stack AI Apps...")
    await mcp_server.stop()

# Initialize FastAPI app
app = FastAPI(
    title="Full-Stack AI Apps",
    description="Deploy AI to AWS, GCP, Azure, Vercel with MLOps, Bedrock, SageMaker, RAG, Agents, MCP",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# Security
security = HTTPBearer()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Full-Stack AI Apps API",
        "version": "1.0.0",
        "description": "Deploy AI to AWS, GCP, Azure, Vercel with MLOps, Bedrock, SageMaker, RAG, Agents, MCP",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "aws": "/api/v1/aws/",
            "gcp": "/api/v1/gcp/", 
            "azure": "/api/v1/azure/",
            "rag": "/api/v1/rag/",
            "agents": "/api/v1/agents/",
            "mcp": "/api/v1/mcp/"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2023-12-01T00:00:00Z",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "services": {
            "aws": await aws_service.health_check(),
            "gcp": await gcp_service.health_check(),
            "azure": await azure_service.health_check(),
            "mcp": await mcp_server.health_check()
        }
    }

# Include routers
from .routes import aws_router, gcp_router, azure_router, rag_router, agents_router, mcp_router

app.include_router(aws_router.router, prefix="/api/v1/aws", tags=["AWS"])
app.include_router(gcp_router.router, prefix="/api/v1/gcp", tags=["GCP"])
app.include_router(azure_router.router, prefix="/api/v1/azure", tags=["Azure"])
app.include_router(rag_router.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(agents_router.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(mcp_router.router, prefix="/api/v1/mcp", tags=["MCP"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development",
        log_config=None  # We use our custom logging setup
    )