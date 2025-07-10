#!/usr/bin/env python3
"""
🧪 Integration Tests
Comprehensive integration testing for the Sacred Geometry AAR Processor system
"""

import asyncio
import os
import tempfile
from datetime import datetime

import pytest

from src.aar_generator import AARGenerator
from src.aar_processor import AARProcessor
from src.compliance_checker import ComplianceChecker
from src.database_manager import DatabaseManager
from src.monitoring_integration import MonitoringIntegration
from src.sacred_geometry_engine import SacredGeometryEngine


class TestFullSystemIntegration:
    """Test full system integration with real components"""

    @pytest.fixture
    async def temp_database(self):
        """Create temporary database for testing"""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_aar.db")
        yield db_path
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)
        os.rmdir(temp_dir)

    @pytest.fixture
    async def integrated_system(self, temp_database):
        """Create fully integrated system with real components"""
        # Initialize real components
        sacred_geometry = SacredGeometryEngine()
        database = DatabaseManager(temp_database)
        monitoring = MonitoringIntegration()
        aar_generator = AARGenerator(sacred_geometry)
        compliance_checker = ComplianceChecker(sacred_geometry)

        processor = AARProcessor(
            sacred_geometry_engine=sacred_geometry,
            database_manager=database,
            monitoring_integration=monitoring,
            aar_generator=aar_generator,
            compliance_checker=compliance_checker,
        )

        # Initialize system
        await processor.initialize()

        yield processor

        # Cleanup
        await processor.shutdown()

    @pytest.mark.asyncio
    async def test_complete_aar_workflow(self, integrated_system):
        """Test complete AAR generation workflow"""
        processor = integrated_system

        # Test data representing a file organization mission
        mission_data = {
            "mission_id": "integration-test-001",
            "mission_type": "file_organization",
            "data": {
                "files_processed": 150,
                "files_organized": 145,
                "errors": 3,
                "warnings": 8,
                "duration": 300,
                "patterns_detected": ["duplicate", "naming_convention"],
                "success_rate": 0.967,
            },
            "timestamp": datetime.now().isoformat(),
        }

        # Process AAR
        result = await processor.process_aar(mission_data)

        # Verify result structure
        assert result.aar_id is not None
        assert result.mission_id == "integration-test-001"
        assert 0.0 <= result.compliance_score <= 1.0
        assert isinstance(result.report_content, dict)
        assert isinstance(result.metadata, dict)

        # Verify AAR content
        assert "file_organization" in result.report_content
        file_org_data = result.report_content["file_organization"]
        assert "success_rate" in file_org_data
        assert "performance_metrics" in file_org_data

        # Verify metadata includes Sacred Geometry analysis
        assert "sacred_geometry" in result.metadata
        assert "processing_time" in result.metadata

    @pytest.mark.asyncio
    async def test_compliance_check_integration(self, integrated_system):
        """Test integrated compliance checking"""
        processor = integrated_system

        # High-quality metrics (should pass compliance)
        high_quality_data = {
            "performance_metrics": {
                "success_rate": 0.95,
                "error_rate": 0.05,
                "response_time": 100,
                "throughput": 1000,
            },
            "quality_metrics": {
                "accuracy": 0.92,
                "precision": 0.89,
                "completeness": 0.96,
                "consistency": 0.93,
            },
            "sacred_geometry_alignment": {
                "circle_completeness": 0.95,
                "triangle_stability": 0.90,
                "spiral_growth": 0.88,
                "golden_ratio_balance": 0.91,
                "fractal_complexity": 0.87,
            },
        }

        result = await processor.check_compliance(high_quality_data)

        assert isinstance(result, dict)
        assert "compliance_score" in result
        assert "level" in result
        assert "passed" in result

        # High-quality data should have good compliance
        assert result["compliance_score"] >= 0.7
        assert result["passed"] is True
        assert result["level"] in ["excellent", "good", "acceptable"]

    @pytest.mark.asyncio
    async def test_low_quality_compliance_check(self, integrated_system):
        """Test compliance check with low-quality data"""
        processor = integrated_system

        # Low-quality metrics (should fail compliance)
        low_quality_data = {
            "performance_metrics": {
                "success_rate": 0.3,
                "error_rate": 0.7,
                "response_time": 5000,
                "throughput": 10,
            },
            "quality_metrics": {
                "accuracy": 0.4,
                "precision": 0.3,
                "completeness": 0.2,
                "consistency": 0.1,
            },
        }

        result = await processor.check_compliance(low_quality_data)

        # Low-quality data should have poor compliance
        assert result["compliance_score"] <= 0.5
        assert result["level"] in ["needs_improvement", "critical"]

    @pytest.mark.asyncio
    async def test_multiple_mission_types(self, integrated_system):
        """Test processing multiple different mission types"""
        processor = integrated_system

        mission_types = [
            {
                "mission_id": "monitoring-001",
                "mission_type": "monitoring_system",
                "data": {
                    "metrics_collected": 1000,
                    "alerts_triggered": 5,
                    "system_health": 0.95,
                    "response_time": 50,
                    "uptime": 0.999,
                },
            },
            {
                "mission_id": "development-001",
                "mission_type": "development",
                "data": {
                    "code_lines": 500,
                    "tests_written": 50,
                    "test_coverage": 0.85,
                    "bugs_fixed": 8,
                    "features_added": 3,
                },
            },
            {
                "mission_id": "deployment-001",
                "mission_type": "deployment",
                "data": {
                    "deployment_time": 600,
                    "rollback_count": 0,
                    "success_rate": 1.0,
                    "services_deployed": 5,
                },
            },
        ]

        results = []
        for mission_data in mission_types:
            mission_data["timestamp"] = datetime.now().isoformat()
            result = await processor.process_aar(mission_data)
            results.append(result)

        # Verify all processed successfully
        assert len(results) == 3

        # Verify each has appropriate content
        for i, result in enumerate(results):
            assert result.mission_id == mission_types[i]["mission_id"]
            mission_type = mission_types[i]["mission_type"]
            assert mission_type in result.report_content

    @pytest.mark.asyncio
    async def test_concurrent_processing_integration(self, integrated_system):
        """Test concurrent processing with real components"""
        processor = integrated_system

        # Create multiple mission data sets
        missions = []
        for i in range(5):
            missions.append(
                {
                    "mission_id": f"concurrent-{i}",
                    "mission_type": "general",
                    "data": {
                        "index": i,
                        "performance": 0.8 + (i * 0.02),
                        "quality": 0.75 + (i * 0.03),
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Process all concurrently
        tasks = [processor.process_aar(mission) for mission in missions]
        results = await asyncio.gather(*tasks)

        # Verify all processed successfully
        assert len(results) == 5

        # Verify each result is unique and valid
        mission_ids = [result.mission_id for result in results]
        assert len(set(mission_ids)) == 5  # All unique

        for result in results:
            assert isinstance(result.compliance_score, (int, float))
            assert 0.0 <= result.compliance_score <= 1.0

    @pytest.mark.asyncio
    async def test_database_persistence_integration(self, integrated_system):
        """Test database persistence integration"""
        processor = integrated_system

        mission_data = {
            "mission_id": "persistence-test-001",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        # Process AAR
        result = await processor.process_aar(mission_data)

        # Verify AAR was stored in database
        database = processor.database_manager
        stored_aar = await database.get_aar(result.aar_id)

        assert stored_aar is not None
        assert stored_aar["aar_id"] == result.aar_id
        assert stored_aar["mission_id"] == result.mission_id

    @pytest.mark.asyncio
    async def test_system_health_monitoring(self, integrated_system):
        """Test system health monitoring integration"""
        processor = integrated_system

        # Check overall system health
        health_status = await processor.health_check()

        assert isinstance(health_status, dict)
        assert "overall_health" in health_status
        assert "components" in health_status
        assert "timestamp" in health_status

        # All components should be healthy in integration test
        assert health_status["overall_health"] == "healthy"

        components = health_status["components"]
        assert "database" in components
        assert "monitoring" in components
        assert "sacred_geometry" in components

        # All individual components should be healthy
        for component, status in components.items():
            assert status["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_error_handling_integration(self, integrated_system):
        """Test error handling in integrated system"""
        processor = integrated_system

        # Test with invalid mission data
        invalid_mission_data = {
            "mission_id": "error-test-001",
            "mission_type": "invalid_type",  # Invalid type
            "data": {},
            "timestamp": datetime.now().isoformat(),
        }

        with pytest.raises(ValueError, match="Unknown mission type"):
            await processor.process_aar(invalid_mission_data)

    @pytest.mark.asyncio
    async def test_sacred_geometry_pattern_validation(self, integrated_system):
        """Test Sacred Geometry pattern validation integration"""
        processor = integrated_system

        # Mission data with strong geometric patterns
        geometric_mission_data = {
            "mission_id": "geometry-test-001",
            "mission_type": "general",
            "data": {
                # Circle pattern (completeness)
                "total_tasks": 100,
                "completed_tasks": 100,
                "completion_rate": 1.0,
                # Triangle pattern (stability)
                "foundation_score": 0.9,
                "structure_score": 0.85,
                "apex_score": 0.8,
                # Golden ratio relationships
                "primary_metric": 161.8,
                "secondary_metric": 100.0,
                # Spiral pattern (growth)
                "growth_iterations": [0.1, 0.2, 0.35, 0.55, 0.8],
                # Overall quality
                "quality_score": 0.95,
            },
            "timestamp": datetime.now().isoformat(),
        }

        result = await processor.process_aar(geometric_mission_data)

        # Strong geometric patterns should yield high compliance
        assert result.compliance_score >= 0.8

        # Verify Sacred Geometry analysis in metadata
        assert "sacred_geometry" in result.metadata
        sacred_geometry_data = result.metadata["sacred_geometry"]
        assert "patterns" in sacred_geometry_data

    @pytest.mark.asyncio
    async def test_monitoring_integration_metrics(self, integrated_system):
        """Test monitoring integration and metrics collection"""
        processor = integrated_system

        # Process multiple AARs to generate metrics
        for i in range(3):
            mission_data = {
                "mission_id": f"metrics-test-{i}",
                "mission_type": "general",
                "data": {"index": i},
                "timestamp": datetime.now().isoformat(),
            }
            await processor.process_aar(mission_data)

        # Verify monitoring system received metrics
        monitoring = processor.monitoring_integration

        # Check if monitoring is tracking processing metrics
        # (This would be more detailed in a real monitoring integration)
        assert await monitoring.is_healthy()

    @pytest.mark.asyncio
    async def test_compliance_trend_analysis(self, integrated_system):
        """Test compliance trend analysis over multiple processes"""
        processor = integrated_system

        # Process AARs with varying quality to create trend
        quality_levels = [0.5, 0.6, 0.7, 0.8, 0.85]
        compliance_scores = []

        for i, quality in enumerate(quality_levels):
            mission_data = {
                "mission_id": f"trend-test-{i}",
                "mission_type": "general",
                "data": {
                    "quality_score": quality,
                    "performance": quality * 0.9,
                    "efficiency": quality * 1.1,
                },
                "timestamp": datetime.now().isoformat(),
            }

            result = await processor.process_aar(mission_data)
            compliance_scores.append(result.compliance_score)

        # Verify improving trend in compliance scores
        # Generally, higher quality input should yield higher compliance
        assert len(compliance_scores) == 5

        # At least some improvement should be visible
        assert compliance_scores[-1] >= compliance_scores[0]

    @pytest.mark.asyncio
    async def test_system_recovery_integration(self, integrated_system):
        """Test system recovery after component failure"""
        processor = integrated_system

        # Test normal operation first
        mission_data = {
            "mission_id": "recovery-test-001",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        result1 = await processor.process_aar(mission_data)
        assert result1 is not None

        # Simulate and test recovery (in real system, this might involve
        # restarting failed components or reconnecting to services)
        health_before = await processor.health_check()
        assert health_before["overall_health"] == "healthy"

        # System should continue to work after "recovery"
        mission_data["mission_id"] = "recovery-test-002"
        result2 = await processor.process_aar(mission_data)
        assert result2 is not None

        health_after = await processor.health_check()
        assert health_after["overall_health"] == "healthy"

    @pytest.mark.asyncio
    async def test_full_system_performance(self, integrated_system):
        """Test full system performance under load"""
        processor = integrated_system

        start_time = datetime.now()

        # Process multiple AARs to test performance
        missions = []
        for i in range(10):
            missions.append(
                {
                    "mission_id": f"performance-test-{i}",
                    "mission_type": "general",
                    "data": {
                        "index": i,
                        "complexity": i % 3,  # Varying complexity
                        "data_size": 100 + (i * 10),
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Process all missions
        results = []
        for mission in missions:
            result = await processor.process_aar(mission)
            results.append(result)

        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        # Verify all processed successfully
        assert len(results) == 10

        # Performance check - should complete within reasonable time
        # (This threshold would be adjusted based on actual performance requirements)
        assert total_time < 30  # 30 seconds for 10 AARs

        # Verify processing rate
        avg_time_per_aar = total_time / 10
        assert avg_time_per_aar < 3  # Less than 3 seconds per AAR on average
