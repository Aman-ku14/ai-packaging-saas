"""
Health Check Endpoint

Provides a simple health check for monitoring and load balancers.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    Returns service status for monitoring tools.
    """
    return {"status": "healthy", "service": "packaging-ai-api"}
