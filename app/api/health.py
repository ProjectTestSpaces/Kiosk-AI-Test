# from fastapi import APIRouter
# from app.db import database

# router = APIRouter(tags=["Health"])

# @router.get("/health", summary="Health Check")
# async def health_check():
#     try:
#         # Check database connectivity
#         await database.execute("SELECT 1")
#         return {"status": "ok", "database": "connected"}
#     except Exception as e:
#         return {"status": "error", "details": str(e)}




from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.db import database
import time
import psutil
import os
from datetime import datetime, timezone
from typing import Dict, Any
import asyncio
import logging

router = APIRouter(tags=["Health"])

logger = logging.getLogger(__name__)

async def check_database_health() -> Dict[str, Any]:
    """Check database connectivity and performance"""
    try:
        start_time = time.time()
        
        # Basic connectivity check
        await database.execute("SELECT 1")
        
        # Check database version and basic info
        version_query = "SELECT version()"
        version_result = await database.fetch_one(version_query)
        
        # Performance check - simple query timing
        perf_start = time.time()
        await database.execute("SELECT COUNT(*) FROM information_schema.tables")
        query_time = (time.time() - perf_start) * 1000  # Convert to ms
        
        total_time = (time.time() - start_time) * 1000
        
        return {
            "status": "healthy",
            "connection_time_ms": round(total_time, 2),
            "query_time_ms": round(query_time, 2),
            "version": version_result[0] if version_result else "unknown",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

def get_system_health() -> Dict[str, Any]:
    """Get system resource information"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # Load average (Unix systems)
        try:
            load_avg = os.getloadavg()
        except (OSError, AttributeError):
            load_avg = None
        
        return {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "used_percent": round((disk.used / disk.total) * 100, 2)
            },
            "load_average": load_avg,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"System health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

@router.get("/health", summary="Basic Health Check")
async def health_check():
    """Basic health check endpoint"""
    try:
        # Quick database connectivity check
        await database.execute("SELECT 1")
        return {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "database": "disconnected",
                "details": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

@router.get("/health/detailed", summary="Detailed Health Check")
async def detailed_health_check():
    """Comprehensive health check with system metrics"""
    health_data = {
        "service": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": time.time() - psutil.boot_time(),
        "checks": {}
    }
    
    overall_healthy = True
    
    # Database health check
    db_health = await check_database_health()
    health_data["checks"]["database"] = db_health
    if db_health["status"] != "healthy":
        overall_healthy = False
    
    # System health check
    system_health = get_system_health()
    health_data["checks"]["system"] = system_health
    if system_health["status"] != "healthy":
        overall_healthy = False
    
    # Check for critical resource usage
    if system_health["status"] == "healthy":
        if system_health["cpu_percent"] > 90:
            health_data["checks"]["system"]["warnings"] = health_data["checks"]["system"].get("warnings", [])
            health_data["checks"]["system"]["warnings"].append("High CPU usage")
        
        if system_health["memory"]["used_percent"] > 90:
            health_data["checks"]["system"]["warnings"] = health_data["checks"]["system"].get("warnings", [])
            health_data["checks"]["system"]["warnings"].append("High memory usage")
    
    # Set overall status
    health_data["service"] = "healthy" if overall_healthy else "unhealthy"
    
    # Return appropriate HTTP status
    if overall_healthy:
        return health_data
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=health_data
        )

@router.get("/health/readiness", summary="Readiness Check")
async def readiness_check():
    """Check if the service is ready to handle requests"""
    try:
        # Check critical dependencies
        await database.execute("SELECT 1")
        
        # Add other readiness checks here (e.g., external APIs, required services)
        
        return {
            "status": "ready",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "checks": {
                "database": "ready"
            }
        }
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "error": str(e)
            }
        )

@router.get("/health/liveness", summary="Liveness Check")
async def liveness_check():
    """Check if the service is alive (minimal check)"""
    return {
        "status": "alive",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.get("/health/database", summary="Database Health Check")
async def database_health_check():
    """Detailed database health information"""
    db_health = await check_database_health()
    
    if db_health["status"] == "healthy":
        return db_health
    else:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=db_health
        )

@router.get("/health/metrics", summary="System Metrics")
async def system_metrics():
    """Get detailed system metrics"""
    try:
        metrics = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "process": {
                "pid": os.getpid(),
                "memory_mb": round(psutil.Process().memory_info().rss / (1024**2), 2),
                "cpu_percent": psutil.Process().cpu_percent(),
                "threads": psutil.Process().num_threads(),
                "open_files": len(psutil.Process().open_files()),
            },
            "system": get_system_health()
        }
        return metrics
    except Exception as e:
        logger.error(f"Metrics collection failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )