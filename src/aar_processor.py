#!/usr/bin/env python3
"""
🌀 Sacred Geometry AAR Processor
Advanced containerized AAR processing system with real-time monitoring integration

This module serves as the core AAR processing engine, implementing Sacred Geometry
patterns for optimal analysis and insight generation.
"""

import asyncio
import os
import signal
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, List, Optional

import structlog
import uvicorn
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel

from src.aar_generator import AARGenerator
from src.compliance_checker import ComplianceChecker
from src.database_manager import DatabaseManager
from src.monitoring_integration import MonitoringIntegration
from src.sacred_geometry_engine import SacredGeometryEngine

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Prometheus metrics
aar_requests_total = Counter(
    "aar_requests_total", "Total AAR processing requests", ["method", "endpoint"]
)
aar_processing_duration = Histogram(
    "aar_processing_duration_seconds", "AAR processing duration"
)
sacred_geometry_compliance = Gauge(
    "sacred_geometry_compliance_percentage", "Sacred Geometry compliance percentage"
)
active_aar_processes = Gauge("active_aar_processes", "Number of active AAR processes")

# Global state
shutdown_event = asyncio.Event()


class AARRequest(BaseModel):
    """AAR generation request model"""

    mission_id: str
    mission_type: str
    context_data: Dict
    sacred_geometry_patterns: List[str] = [
        "circle",
        "triangle",
        "spiral",
        "golden_ratio",
        "fractal",
    ]
    compliance_target: float = 95.0
    priority: str = "normal"


class AARResponse(BaseModel):
    """AAR generation response model"""

    aar_id: str
    mission_id: str
    status: str
    sacred_geometry_compliance: float
    generated_at: datetime
    processing_duration: float
    report_url: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    timestamp: datetime
    sacred_geometry_engine: str
    database_connection: str
    monitoring_integration: str
    compliance_level: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with Sacred Geometry initialization"""
    logger.info("🌀 Sacred Geometry AAR Processor starting...")

    # Initialize Sacred Geometry engine
    app.state.sacred_geometry = SacredGeometryEngine()
    await app.state.sacred_geometry.initialize()

    # Initialize AAR generator
    app.state.aar_generator = AARGenerator(app.state.sacred_geometry)

    # Initialize monitoring integration
    app.state.monitoring = MonitoringIntegration()
    await app.state.monitoring.connect()

    # Initialize database manager
    app.state.database = DatabaseManager()
    await app.state.database.initialize()

    # Initialize compliance checker
    app.state.compliance = ComplianceChecker(app.state.sacred_geometry)

    logger.info("✅ Sacred Geometry AAR Processor initialized successfully")

    yield

    # Cleanup
    logger.info("🔄 Sacred Geometry AAR Processor shutting down...")
    await app.state.monitoring.disconnect()
    await app.state.database.close()
    logger.info("✅ Sacred Geometry AAR Processor shutdown complete")


# Create FastAPI application with Sacred Geometry principles
app = FastAPI(
    title="Sacred Geometry AAR Processor",
    description="Advanced containerized AAR processing system with real-time monitoring integration",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Sacred Geometry health check endpoint"""
    try:
        # Check Sacred Geometry engine
        sg_status = "healthy" if app.state.sacred_geometry.is_healthy() else "unhealthy"

        # Check database connection
        db_status = "healthy" if await app.state.database.is_healthy() else "unhealthy"

        # Check monitoring integration
        monitoring_status = (
            "healthy" if app.state.monitoring.is_connected() else "unhealthy"
        )

        # Get current compliance level
        compliance_level = await app.state.compliance.get_current_compliance()

        status = (
            "healthy"
            if all(
                [
                    sg_status == "healthy",
                    db_status == "healthy",
                    monitoring_status == "healthy",
                ]
            )
            else "unhealthy"
        )

        return HealthResponse(
            status=status,
            timestamp=datetime.now(),
            sacred_geometry_engine=sg_status,
            database_connection=db_status,
            monitoring_integration=monitoring_status,
            compliance_level=compliance_level,
        )
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail="Health check failed")


@app.post("/aar/generate", response_model=AARResponse)
async def generate_aar(request: AARRequest, background_tasks: BackgroundTasks):
    """Generate AAR following Sacred Geometry patterns"""
    start_time = datetime.now()
    aar_requests_total.labels(method="POST", endpoint="/aar/generate").inc()
    active_aar_processes.inc()

    try:
        logger.info(
            "🎯 Starting AAR generation",
            mission_id=request.mission_id,
            patterns=request.sacred_geometry_patterns,
        )

        # Validate Sacred Geometry patterns
        if not app.state.sacred_geometry.validate_patterns(
            request.sacred_geometry_patterns
        ):
            raise HTTPException(
                status_code=400, detail="Invalid Sacred Geometry patterns"
            )

        # Generate AAR ID using Sacred Geometry principles
        aar_id = app.state.sacred_geometry.generate_aar_id(request.mission_id)

        # Process AAR generation
        aar_result = await app.state.aar_generator.generate(
            aar_id=aar_id,
            mission_id=request.mission_id,
            mission_type=request.mission_type,
            context_data=request.context_data,
            patterns=request.sacred_geometry_patterns,
            compliance_target=request.compliance_target,
        )

        # Calculate processing duration
        processing_duration = (datetime.now() - start_time).total_seconds()
        aar_processing_duration.observe(processing_duration)

        # Update Sacred Geometry compliance metric
        sacred_geometry_compliance.set(aar_result.compliance_score)

        # Store AAR in database
        await app.state.database.store_aar(aar_result)

        # Send metrics to monitoring system
        background_tasks.add_task(
            app.state.monitoring.send_aar_metrics,
            aar_id,
            aar_result.compliance_score,
            processing_duration,
        )

        logger.info(
            "✅ AAR generation completed",
            aar_id=aar_id,
            compliance=aar_result.compliance_score,
            duration=processing_duration,
        )

        return AARResponse(
            aar_id=aar_id,
            mission_id=request.mission_id,
            status="completed",
            sacred_geometry_compliance=aar_result.compliance_score,
            generated_at=datetime.now(),
            processing_duration=processing_duration,
            report_url=f"/aar/{aar_id}/report",
        )

    except Exception as e:
        logger.error(
            "AAR generation failed", mission_id=request.mission_id, error=str(e)
        )
        raise HTTPException(status_code=500, detail=f"AAR generation failed: {str(e)}")

    finally:
        active_aar_processes.dec()


@app.get("/aar/{aar_id}/status")
async def get_aar_status(aar_id: str):
    """Get AAR processing status"""
    try:
        status = await app.state.database.get_aar_status(aar_id)
        if not status:
            raise HTTPException(status_code=404, detail="AAR not found")
        return status
    except Exception as e:
        logger.error("Failed to get AAR status", aar_id=aar_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get AAR status")


@app.get("/aar/{aar_id}/report")
async def get_aar_report(aar_id: str):
    """Get generated AAR report"""
    try:
        report = await app.state.database.get_aar_report(aar_id)
        if not report:
            raise HTTPException(status_code=404, detail="AAR report not found")
        return report
    except Exception as e:
        logger.error("Failed to get AAR report", aar_id=aar_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get AAR report")


@app.get("/sacred-geometry/compliance")
async def get_compliance_status():
    """Get current Sacred Geometry compliance status"""
    try:
        compliance_data = await app.state.compliance.get_detailed_compliance()
        return compliance_data
    except Exception as e:
        logger.error("Failed to get compliance status", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get compliance status")


@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()


@app.post("/sacred-geometry/validate")
async def validate_sacred_geometry(data: Dict):
    """Validate data against Sacred Geometry patterns"""
    try:
        validation_result = await app.state.sacred_geometry.validate_data(data)
        return validation_result
    except Exception as e:
        logger.error("Sacred Geometry validation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Validation failed")


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("🔄 Received shutdown signal", signal=signum)
    shutdown_event.set()


async def main():
    """Main application entry point"""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info")

    logger.info("🌀 Starting Sacred Geometry AAR Processor", host=host, port=port)

    # Create server config
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level=log_level,
        access_log=True,
        loop="asyncio",
    )

    # Create and run server
    server = uvicorn.Server(config)

    try:
        await server.serve()
    except KeyboardInterrupt:
        logger.info("🔄 Shutting down Sacred Geometry AAR Processor")
    finally:
        logger.info("✅ Sacred Geometry AAR Processor stopped")


if __name__ == "__main__":
    asyncio.run(main())
