"""
🧪 Test Configuration and Shared Fixtures
Pytest configuration and shared test fixtures for AAR processor tests
"""

import asyncio
import os
import tempfile
from typing import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
import structlog

# Configure structured logging for tests
structlog.configure(
    processors=[structlog.stdlib.filter_by_level, structlog.dev.ConsoleRenderer()],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


@pytest.fixture
def temp_db_path() -> Generator[str, None, None]:
    """Create a temporary database file for testing"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        temp_path = temp_file.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
async def database_manager():
    """Create a database manager instance for testing"""
    from src.database_manager import DatabaseManager

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        temp_path = temp_file.name

    db_manager = DatabaseManager(db_path=temp_path)
    await db_manager.initialize()

    yield db_manager

    await db_manager.close()
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def mock_aiohttp_session():
    """Mock aiohttp session for testing monitoring integration"""
    session = MagicMock()

    # Mock response object
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={
            "status": "green",
            "cluster_name": "test-cluster",
            "number_of_nodes": 1,
        }
    )
    mock_response.__aenter__ = AsyncMock(return_value=mock_response)
    mock_response.__aexit__ = AsyncMock(return_value=None)

    session.get = AsyncMock(return_value=mock_response)
    session.post = AsyncMock(return_value=mock_response)
    session.close = AsyncMock()

    return session


@pytest.fixture
async def monitoring_integration(mock_aiohttp_session):
    """Create monitoring integration instance for testing"""
    from src.monitoring_integration import MonitoringIntegration

    integration = MonitoringIntegration()
    integration.session = mock_aiohttp_session
    integration.connected = True

    yield integration

    await integration.disconnect()


@pytest.fixture
def sacred_geometry_engine():
    """Create Sacred Geometry engine for testing"""
    from src.sacred_geometry_engine import SacredGeometryEngine

    return SacredGeometryEngine()


@pytest.fixture
async def aar_generator(sacred_geometry_engine):
    """Create AAR generator for testing"""
    from src.aar_generator import AARGenerator

    return AARGenerator(sacred_geometry_engine)


@pytest.fixture
def compliance_checker():
    """Create compliance checker for testing"""
    from src.compliance_checker import ComplianceChecker

    return ComplianceChecker()


@pytest.fixture
def sample_context_data():
    """Sample context data for testing AAR generation"""
    return {
        "mission_id": "TEST-001",
        "mission_type": "file_organization",
        "description": "Test file organization mission",
        "objectives": [
            "Organize loose files",
            "Apply Sacred Geometry principles",
            "Improve workspace structure",
        ],
        "files_processed": ["file1.txt", "file2.py", "file3.md"],
        "directories_created": ["organized/", "backup/", "logs/"],
        "duration": "00:15:30",
        "success_rate": 95.5,
        "status": "completed",
        "achievements": [
            "Successfully organized 147 files",
            "Applied Golden Ratio naming conventions",
            "Improved accessibility by 40%",
        ],
        "challenges": [
            "Large files required special handling",
            "Some legacy naming conventions encountered",
        ],
        "lessons_learned": [
            "Golden Ratio proportions improve file discovery",
            "Spiral organization enhances workflow efficiency",
        ],
    }


@pytest.fixture
def sample_aar_request():
    """Sample AAR generation request"""
    return {
        "mission_id": "TEST-001",
        "mission_type": "file_organization",
        "context_data": {
            "description": "Test mission for unit testing",
            "files_processed": 50,
            "success_rate": 95.0,
        },
        "patterns": ["circle", "triangle", "spiral"],
        "compliance_target": 95.0,
    }


@pytest.fixture
def mock_prometheus_metrics():
    """Mock Prometheus metrics for testing"""
    metrics_mock = MagicMock()
    metrics_mock.inc = MagicMock()
    metrics_mock.set = MagicMock()
    metrics_mock.observe = MagicMock()

    return {
        "aar_requests_total": metrics_mock,
        "aar_processing_duration": metrics_mock,
        "sacred_geometry_compliance": metrics_mock,
        "active_aar_processes": metrics_mock,
    }


@pytest.fixture
async def test_client():
    """Create FastAPI test client"""
    from fastapi.testclient import TestClient

    from src.aar_processor import app

    with TestClient(app) as client:
        yield client


@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# Test data fixtures
@pytest.fixture
def valid_sacred_geometry_data():
    """Valid data that should pass Sacred Geometry validation"""
    return {
        "circle": {
            "completeness": 0.95,
            "coverage": ["initialization", "processing", "completion", "validation"],
        },
        "triangle": {
            "stability": 0.88,
            "components": ["input", "processing", "output"],
        },
        "spiral": {"progression": 0.92, "iterations": 5, "enhancement_factor": 1.618},
        "golden_ratio": {"proportion": 1.618, "optimization_score": 0.89},
        "fractal": {"self_similarity": 0.83, "scales": 3, "recursion_depth": 4},
    }


@pytest.fixture
def invalid_sacred_geometry_data():
    """Invalid data that should fail Sacred Geometry validation"""
    return {
        "circle": {
            "completeness": 0.45,  # Below threshold
            "coverage": ["initialization", "processing"],  # Incomplete
        },
        "triangle": {
            "stability": 0.35,  # Poor stability
            "components": ["input"],  # Missing components
        },
        "spiral": {
            "progression": 0.25,  # Poor progression
            "iterations": 1,  # Too few iterations
            "enhancement_factor": 1.0,  # Not golden ratio
        },
    }


# Test utilities
def assert_sacred_geometry_compliance(result: dict, min_score: float = 0.7):
    """Helper to assert Sacred Geometry compliance in test results"""
    assert "sacred_geometry_analysis" in result
    sg_analysis = result["sacred_geometry_analysis"]

    assert "patterns_detected" in sg_analysis
    assert "circle_completeness" in sg_analysis
    assert "triangle_stability" in sg_analysis
    assert "spiral_progression" in sg_analysis
    assert "golden_ratio_optimization" in sg_analysis

    # Check minimum compliance scores
    assert sg_analysis["circle_completeness"] >= min_score
    assert sg_analysis["triangle_stability"] >= min_score
    assert sg_analysis["spiral_progression"] >= min_score


def assert_aar_structure(aar_result: dict):
    """Helper to assert proper AAR structure"""
    required_sections = [
        "aar_id",
        "mission_id",
        "report_type",
        "generated_at",
        "executive_summary",
        "sacred_geometry_analysis",
        "achievements",
        "challenges",
        "lessons_learned",
        "recommendations",
    ]

    for section in required_sections:
        assert section in aar_result, f"Missing required section: {section}"

    # Check executive summary structure
    exec_summary = aar_result["executive_summary"]
    assert "mission_overview" in exec_summary
    assert "compliance_score" in exec_summary

    # Check recommendations structure
    recommendations = aar_result["recommendations"]
    assert "immediate" in recommendations
    assert "medium_term" in recommendations
    assert "long_term" in recommendations
