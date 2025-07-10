"""
🧪 Database Manager Unit Tests
Comprehensive tests for AAR database operations and persistence
"""

import os
import tempfile

import pytest

from src.database_manager import DatabaseManager


class TestDatabaseManager:
    """Test suite for DatabaseManager class"""

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
    async def test_initialization_creates_database(self):
        """Test that database initialization creates the database file"""
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

        await db_manager.close()

    @pytest.mark.asyncio
    async def test_create_tables(self, database_manager):
        """Test that all required tables are created"""
        # Get table names from database
        cursor = database_manager.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        # Check that required tables exist
        expected_tables = [
            "aar_reports",
            "aar_missions",
            "compliance_scores",
            "monitoring_events",
        ]
        for table in expected_tables:
            assert table in tables, f"Table {table} was not created"

    @pytest.mark.asyncio
    async def test_health_check_healthy_database(self, database_manager):
        """Test health check with healthy database"""
        is_healthy = await database_manager.is_healthy()
        assert is_healthy is True

    @pytest.mark.asyncio
    async def test_health_check_closed_database(self):
        """Test health check with closed database"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name

        db_manager = DatabaseManager(db_path=temp_path)
        await db_manager.initialize()
        await db_manager.close()

        is_healthy = await db_manager.is_healthy()
        assert is_healthy is False

        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_store_aar_report(self, database_manager, sample_context_data):
        """Test storing AAR report in database"""
        aar_data = {
            "aar_id": "TEST-AAR-001",
            "mission_id": "TEST-MISSION-001",
            "report_type": "file_organization",
            "generated_at": datetime.now().isoformat(),
            "executive_summary": {
                "mission_overview": "Test mission overview",
                "compliance_score": 95.5,
            },
            "sacred_geometry_analysis": {
                "circle_completeness": 0.95,
                "triangle_stability": 0.88,
                "spiral_progression": 0.92,
                "golden_ratio_optimization": 0.89,
            },
            "achievements": ["Test achievement 1", "Test achievement 2"],
            "challenges": ["Test challenge 1"],
            "lessons_learned": ["Test lesson 1"],
            "recommendations": {
                "immediate": ["Test immediate action"],
                "medium_term": ["Test medium term action"],
                "long_term": ["Test long term action"],
            },
        }

        # Store the AAR report
        await database_manager.store_aar_report(aar_data)

        # Verify it was stored correctly
        retrieved_report = await database_manager.get_aar_report("TEST-AAR-001")

        assert retrieved_report is not None
        assert retrieved_report["aar_id"] == "TEST-AAR-001"
        assert retrieved_report["mission_id"] == "TEST-MISSION-001"
        assert retrieved_report["report_type"] == "file_organization"

    @pytest.mark.asyncio
    async def test_get_nonexistent_aar_report(self, database_manager):
        """Test retrieving non-existent AAR report returns None"""
        result = await database_manager.get_aar_report("NONEXISTENT-ID")
        assert result is None

    @pytest.mark.asyncio
    async def test_store_mission_data(self, database_manager, sample_context_data):
        """Test storing mission data"""
        mission_data = {
            "mission_id": "TEST-MISSION-002",
            "mission_type": "development",
            "status": "in_progress",
            "context_data": sample_context_data,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        await database_manager.store_mission_data(mission_data)

        # Verify storage
        retrieved_mission = await database_manager.get_mission_data("TEST-MISSION-002")

        assert retrieved_mission is not None
        assert retrieved_mission["mission_id"] == "TEST-MISSION-002"
        assert retrieved_mission["mission_type"] == "development"
        assert retrieved_mission["status"] == "in_progress"

    @pytest.mark.asyncio
    async def test_store_compliance_score(self, database_manager):
        """Test storing compliance scores"""
        compliance_data = {
            "aar_id": "TEST-AAR-003",
            "overall_score": 94.5,
            "circle_score": 95.2,
            "triangle_score": 88.7,
            "spiral_score": 92.1,
            "golden_ratio_score": 89.3,
            "fractal_score": 91.8,
            "calculated_at": datetime.now().isoformat(),
        }

        await database_manager.store_compliance_score(compliance_data)

        # Verify storage
        retrieved_scores = await database_manager.get_compliance_scores("TEST-AAR-003")

        assert retrieved_scores is not None
        assert retrieved_scores["overall_score"] == 94.5
        assert retrieved_scores["circle_score"] == 95.2

    @pytest.mark.asyncio
    async def test_store_monitoring_event(self, database_manager):
        """Test storing monitoring events"""
        event_data = {
            "event_id": "EVENT-001",
            "event_type": "aar_generated",
            "aar_id": "TEST-AAR-004",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "processing_duration": 2.5,
                "compliance_score": 93.2,
                "memory_usage": 45.6,
            },
            "status": "success",
        }

        await database_manager.store_monitoring_event(event_data)

        # Verify storage
        retrieved_events = await database_manager.get_monitoring_events("TEST-AAR-004")

        assert len(retrieved_events) == 1
        assert retrieved_events[0]["event_type"] == "aar_generated"
        assert retrieved_events[0]["status"] == "success"

    @pytest.mark.asyncio
    async def test_list_aar_reports(self, database_manager):
        """Test listing AAR reports with pagination"""
        # Store multiple reports
        for i in range(5):
            aar_data = {
                "aar_id": f"TEST-AAR-LIST-{i:03d}",
                "mission_id": f"TEST-MISSION-{i:03d}",
                "report_type": "general",
                "generated_at": datetime.now().isoformat(),
                "executive_summary": {"compliance_score": 90.0 + i},
                "sacred_geometry_analysis": {},
                "achievements": [],
                "challenges": [],
                "lessons_learned": [],
                "recommendations": {},
            }
            await database_manager.store_aar_report(aar_data)

        # Test listing with pagination
        reports = await database_manager.list_aar_reports(limit=3, offset=0)
        assert len(reports) == 3

        reports_page_2 = await database_manager.list_aar_reports(limit=3, offset=3)
        assert len(reports_page_2) == 2

    @pytest.mark.asyncio
    async def test_search_aar_reports(self, database_manager):
        """Test searching AAR reports by criteria"""
        # Store test reports with different types
        test_reports = [
            {
                "aar_id": "SEARCH-001",
                "mission_id": "MISSION-001",
                "report_type": "file_organization",
                "generated_at": datetime.now().isoformat(),
                "executive_summary": {"compliance_score": 95.0},
                "sacred_geometry_analysis": {},
                "achievements": [],
                "challenges": [],
                "lessons_learned": [],
                "recommendations": {},
            },
            {
                "aar_id": "SEARCH-002",
                "mission_id": "MISSION-002",
                "report_type": "deployment",
                "generated_at": datetime.now().isoformat(),
                "executive_summary": {"compliance_score": 88.0},
                "sacred_geometry_analysis": {},
                "achievements": [],
                "challenges": [],
                "lessons_learned": [],
                "recommendations": {},
            },
        ]

        for report in test_reports:
            await database_manager.store_aar_report(report)

        # Search by report type
        file_org_reports = await database_manager.search_aar_reports(
            report_type="file_organization"
        )
        assert len(file_org_reports) >= 1
        assert file_org_reports[0]["report_type"] == "file_organization"

        # Search by mission ID
        mission_reports = await database_manager.search_aar_reports(
            mission_id="MISSION-001"
        )
        assert len(mission_reports) >= 1
        assert mission_reports[0]["mission_id"] == "MISSION-001"

    @pytest.mark.asyncio
    async def test_update_aar_report(self, database_manager):
        """Test updating existing AAR report"""
        # Create initial report
        original_report = {
            "aar_id": "UPDATE-TEST-001",
            "mission_id": "UPDATE-MISSION-001",
            "report_type": "general",
            "generated_at": datetime.now().isoformat(),
            "executive_summary": {"compliance_score": 85.0},
            "sacred_geometry_analysis": {},
            "achievements": ["Initial achievement"],
            "challenges": [],
            "lessons_learned": [],
            "recommendations": {},
        }

        await database_manager.store_aar_report(original_report)

        # Update the report
        updated_data = {
            "executive_summary": {"compliance_score": 95.0},
            "achievements": ["Initial achievement", "Updated achievement"],
        }

        await database_manager.update_aar_report("UPDATE-TEST-001", updated_data)

        # Verify update
        retrieved_report = await database_manager.get_aar_report("UPDATE-TEST-001")
        assert retrieved_report["executive_summary"]["compliance_score"] == 95.0
        assert len(retrieved_report["achievements"]) == 2

    @pytest.mark.asyncio
    async def test_delete_aar_report(self, database_manager):
        """Test deleting AAR report"""
        # Create report to delete
        report_to_delete = {
            "aar_id": "DELETE-TEST-001",
            "mission_id": "DELETE-MISSION-001",
            "report_type": "general",
            "generated_at": datetime.now().isoformat(),
            "executive_summary": {"compliance_score": 90.0},
            "sacred_geometry_analysis": {},
            "achievements": [],
            "challenges": [],
            "lessons_learned": [],
            "recommendations": {},
        }

        await database_manager.store_aar_report(report_to_delete)

        # Verify it exists
        retrieved_report = await database_manager.get_aar_report("DELETE-TEST-001")
        assert retrieved_report is not None

        # Delete the report
        await database_manager.delete_aar_report("DELETE-TEST-001")

        # Verify deletion
        deleted_report = await database_manager.get_aar_report("DELETE-TEST-001")
        assert deleted_report is None

    @pytest.mark.asyncio
    async def test_database_error_handling(self):
        """Test database error handling for invalid operations"""
        # Test with invalid database path
        invalid_db_manager = DatabaseManager(db_path="/invalid/path/database.db")

        with pytest.raises(Exception):
            await invalid_db_manager.initialize()

    @pytest.mark.asyncio
    async def test_json_serialization_in_storage(self, database_manager):
        """Test proper JSON serialization of complex data structures"""
        complex_report = {
            "aar_id": "JSON-TEST-001",
            "mission_id": "JSON-MISSION-001",
            "report_type": "general",
            "generated_at": datetime.now().isoformat(),
            "executive_summary": {
                "compliance_score": 92.5,
                "nested_data": {
                    "metrics": [1, 2, 3, 4, 5],
                    "flags": {"feature_a": True, "feature_b": False},
                },
            },
            "sacred_geometry_analysis": {
                "patterns": ["circle", "triangle", "spiral"],
                "scores": {"circle": 0.95, "triangle": 0.88},
            },
            "achievements": ["Achievement 1", "Achievement 2"],
            "challenges": [],
            "lessons_learned": [],
            "recommendations": {
                "immediate": ["Action 1"],
                "medium_term": ["Action 2", "Action 3"],
                "long_term": [],
            },
        }

        await database_manager.store_aar_report(complex_report)

        # Retrieve and verify complex data integrity
        retrieved_report = await database_manager.get_aar_report("JSON-TEST-001")

        assert retrieved_report["executive_summary"]["nested_data"]["metrics"] == [
            1,
            2,
            3,
            4,
            5,
        ]
        assert (
            retrieved_report["executive_summary"]["nested_data"]["flags"]["feature_a"]
            is True
        )
        assert retrieved_report["sacred_geometry_analysis"]["patterns"] == [
            "circle",
            "triangle",
            "spiral",
        ]
        assert len(retrieved_report["recommendations"]["medium_term"]) == 2

    @pytest.mark.asyncio
    async def test_connection_management(self, temp_db_path):
        """Test proper connection management and cleanup"""
        db_manager = DatabaseManager(db_path=temp_db_path)

        # Initially no connection
        assert db_manager.connection is None

        # Initialize creates connection
        await db_manager.initialize()
        assert db_manager.connection is not None

        # Close removes connection
        await db_manager.close()
        assert db_manager.connection is None

        # Can reinitialize after close
        await db_manager.initialize()
        assert db_manager.connection is not None

        await db_manager.close()

    @pytest.mark.asyncio
    async def test_concurrent_access(self, database_manager):
        """Test handling of concurrent database operations"""
        import asyncio

        # Create multiple concurrent write operations
        async def store_report(report_id):
            report = {
                "aar_id": f"CONCURRENT-{report_id}",
                "mission_id": f"MISSION-{report_id}",
                "report_type": "general",
                "generated_at": datetime.now().isoformat(),
                "executive_summary": {"compliance_score": 90.0},
                "sacred_geometry_analysis": {},
                "achievements": [],
                "challenges": [],
                "lessons_learned": [],
                "recommendations": {},
            }
            await database_manager.store_aar_report(report)
            return report_id

        # Execute concurrent operations
        tasks = [store_report(i) for i in range(10)]
        results = await asyncio.gather(*tasks)

        # Verify all operations completed
        assert len(results) == 10

        # Verify all reports were stored
        for i in range(10):
            report = await database_manager.get_aar_report(f"CONCURRENT-{i}")
            assert report is not None
            assert report["mission_id"] == f"MISSION-{i}"
