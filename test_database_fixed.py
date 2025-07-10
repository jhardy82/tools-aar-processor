#!/usr/bin/env python3
"""
🧪 Fixed Database Manager Tests
Tests that actually match the real API
"""

import os
import tempfile

import pytest

from src.aar_generator import AARResult
from src.database_manager import DatabaseManager


class TestDatabaseManagerFixed:
    """Test suite for DatabaseManager class - FIXED VERSION"""

    @pytest.fixture
    async def temp_db_manager(self):
        """Create a temporary database manager for testing"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name

        db_manager = DatabaseManager(db_path=temp_path)
        await db_manager.initialize()

        yield db_manager

        await db_manager.close()
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_database_initialization(self):
        """Test database initialization works"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name

        # Database file should not exist initially
        assert not os.path.exists(temp_path)

        db_manager = DatabaseManager(db_path=temp_path)
        await db_manager.initialize()

        # Database file should exist after initialization
        assert os.path.exists(temp_path)
        assert db_manager.connection is not None

        # Cleanup
        await db_manager.close()
        os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_health_check(self, temp_db_manager):
        """Test database health check"""
        health = await temp_db_manager.is_healthy()
        assert health is True

    @pytest.mark.asyncio
    async def test_store_and_retrieve_aar(self, temp_db_manager):
        """Test storing and retrieving AAR data"""
        # Create test AAR
        aar_result = AARResult(
            aar_id="test-store-123",
            mission_id="mission-store-456",
            compliance_score=0.92,
            report_content={"status": "success", "details": "test data"},
            metadata={"version": "1.0", "test": True},
        )

        # Store AAR
        success = await temp_db_manager.store_aar(aar_result)
        assert success is True

        # Retrieve AAR status
        status = await temp_db_manager.get_aar_status("test-store-123")
        assert status is not None
        assert status["aar_id"] == "test-store-123"
        assert status["mission_id"] == "mission-store-456"
        assert status["compliance_score"] == 0.92

        # Retrieve AAR report
        report = await temp_db_manager.get_aar_report("test-store-123")
        assert report is not None
        assert report["aar_id"] == "test-store-123"
        assert "report_content" in report

    @pytest.mark.asyncio
    async def test_list_aars(self, temp_db_manager):
        """Test listing AARs"""
        # Store multiple AARs
        for i in range(3):
            aar_result = AARResult(
                aar_id=f"test-list-{i}",
                mission_id=f"mission-{i}",
                compliance_score=0.8 + (i * 0.05),
                report_content={"index": i},
                metadata={"test": True},
            )
            await temp_db_manager.store_aar(aar_result)

        # List AARs
        aars = await temp_db_manager.list_aars(limit=10)
        assert len(aars) == 3

        # Verify the AARs are ordered correctly (most recent first)
        assert aars[0]["aar_id"] == "test-list-2"

    @pytest.mark.asyncio
    async def test_compliance_stats(self, temp_db_manager):
        """Test compliance statistics"""
        # Store AARs with different compliance scores
        scores = [0.7, 0.8, 0.9, 0.95]
        for i, score in enumerate(scores):
            aar_result = AARResult(
                aar_id=f"test-stats-{i}",
                mission_id=f"mission-stats-{i}",
                compliance_score=score,
                report_content={},
                metadata={},
            )
            await temp_db_manager.store_aar(aar_result)

        # Get compliance stats
        stats = await temp_db_manager.get_compliance_stats()

        assert "total_aars" in stats
        assert "average_compliance" in stats
        assert "min_compliance" in stats
        assert "max_compliance" in stats

        assert stats["total_aars"] == 4
        assert stats["min_compliance"] == 0.7
        assert stats["max_compliance"] == 0.95

    @pytest.mark.asyncio
    async def test_nonexistent_aar(self, temp_db_manager):
        """Test retrieving non-existent AAR"""
        status = await temp_db_manager.get_aar_status("nonexistent-123")
        assert status is None

        report = await temp_db_manager.get_aar_report("nonexistent-456")
        assert report is None
