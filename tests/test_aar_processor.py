#!/usr/bin/env python3
"""
🧪 AAR Processor Unit Tests
Comprehensive testing for the main AAR processor FastAPI application
"""

import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.aar_generator import AARGenerator, AARResult
from src.aar_processor import AARProcessor, app
from src.compliance_checker import ComplianceChecker
from src.database_manager import DatabaseManager
from src.monitoring_integration import MonitoringIntegration
from src.sacred_geometry_engine import SacredGeometryEngine


class TestAARProcessorAPI:
    """Test AAR Processor FastAPI endpoints"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["status"] == "healthy"

    def test_metrics_endpoint(self, client):
        """Test Prometheus metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert (
            response.headers["content-type"]
            == "text/plain; version=0.0.4; charset=utf-8"
        )

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert data["service"] == "Sacred Geometry AAR Processor"

    @patch("src.aar_processor.processor")
    def test_process_aar_endpoint(self, mock_processor, client):
        """Test AAR processing endpoint"""
        # Mock the processor
        mock_result = AARResult(
            aar_id="test-123",
            mission_id="mission-456",
            compliance_score=0.85,
            report_content={"status": "success"},
            metadata={"version": "1.0"},
        )
        mock_processor.process_aar = AsyncMock(return_value=mock_result)

        mission_data = {
            "mission_id": "mission-456",
            "mission_type": "file_organization",
            "data": {"files": 100},
            "timestamp": datetime.now().isoformat(),
        }

        response = client.post("/process", json=mission_data)
        assert response.status_code == 200

        data = response.json()
        assert "aar_id" in data
        assert "mission_id" in data
        assert "compliance_score" in data
        assert data["mission_id"] == "mission-456"

    @patch("src.aar_processor.processor")
    def test_process_aar_endpoint_error(self, mock_processor, client):
        """Test AAR processing endpoint error handling"""
        # Mock processor to raise exception
        mock_processor.process_aar = AsyncMock(
            side_effect=Exception("Processing error")
        )

        mission_data = {
            "mission_id": "mission-456",
            "mission_type": "invalid",
            "data": {},
            "timestamp": datetime.now().isoformat(),
        }

        response = client.post("/process", json=mission_data)
        assert response.status_code == 500

        data = response.json()
        assert "detail" in data

    @patch("src.aar_processor.processor")
    def test_compliance_check_endpoint(self, mock_processor, client):
        """Test compliance check endpoint"""
        mock_processor.check_compliance = AsyncMock(
            return_value={
                "compliance_score": 0.87,
                "level": "good",
                "passed": True,
                "details": {"pattern_scores": {"circle": 0.9}},
            }
        )

        test_data = {"performance": 0.9, "quality": 0.85, "efficiency": 0.8}

        response = client.post("/compliance/check", json=test_data)
        assert response.status_code == 200

        data = response.json()
        assert "compliance_score" in data
        assert "level" in data
        assert "passed" in data
        assert data["compliance_score"] == 0.87

    def test_invalid_json_handling(self, client):
        """Test handling of invalid JSON requests"""
        response = client.post("/process", data="invalid json")
        assert response.status_code == 422  # Unprocessable Entity

    def test_missing_required_fields(self, client):
        """Test handling of missing required fields"""
        incomplete_data = {
            "mission_type": "general"
            # Missing mission_id
        }

        response = client.post("/process", json=incomplete_data)
        assert response.status_code == 422

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/")
        assert "access-control-allow-origin" in response.headers


class TestAARProcessorCore:
    """Test AAR Processor core functionality"""

    @pytest.fixture
    def mock_components(self):
        """Create mock components"""
        sacred_geometry = MagicMock(spec=SacredGeometryEngine)
        sacred_geometry.initialize = AsyncMock()
        sacred_geometry.calculate_compliance = AsyncMock(return_value=0.85)

        database = MagicMock(spec=DatabaseManager)
        database.initialize = AsyncMock()
        database.is_healthy = AsyncMock(return_value=True)
        database.store_aar = AsyncMock()

        monitoring = MagicMock(spec=MonitoringIntegration)
        monitoring.initialize = AsyncMock()
        monitoring.is_healthy = AsyncMock(return_value=True)
        monitoring.send_metric = AsyncMock()

        aar_generator = MagicMock(spec=AARGenerator)
        aar_generator.generate_aar = AsyncMock()

        compliance_checker = MagicMock(spec=ComplianceChecker)
        compliance_checker.check_compliance = AsyncMock()

        return {
            "sacred_geometry": sacred_geometry,
            "database": database,
            "monitoring": monitoring,
            "aar_generator": aar_generator,
            "compliance_checker": compliance_checker,
        }

    @pytest.fixture
    def processor(self, mock_components):
        """Create AAR processor with mocked components"""
        return AARProcessor(
            sacred_geometry_engine=mock_components["sacred_geometry"],
            database_manager=mock_components["database"],
            monitoring_integration=mock_components["monitoring"],
            aar_generator=mock_components["aar_generator"],
            compliance_checker=mock_components["compliance_checker"],
        )

    @pytest.mark.asyncio
    async def test_processor_initialization(self, processor, mock_components):
        """Test processor initialization"""
        await processor.initialize()

        # Verify all components were initialized
        mock_components["sacred_geometry"].initialize.assert_called_once()
        mock_components["database"].initialize.assert_called_once()
        mock_components["monitoring"].initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_processor_health_check(self, processor, mock_components):
        """Test processor health check"""
        await processor.initialize()

        health_status = await processor.health_check()

        assert isinstance(health_status, dict)
        assert "overall_health" in health_status
        assert "components" in health_status
        assert "timestamp" in health_status

        # Verify component health was checked
        mock_components["database"].is_healthy.assert_called()
        mock_components["monitoring"].is_healthy.assert_called()

    @pytest.mark.asyncio
    async def test_process_aar_success(self, processor, mock_components):
        """Test successful AAR processing"""
        await processor.initialize()

        # Configure mocks
        mock_result = AARResult(
            aar_id="test-123",
            mission_id="mission-456",
            compliance_score=0.85,
            report_content={"status": "success"},
            metadata={"version": "1.0"},
        )
        mock_components["aar_generator"].generate_aar.return_value = mock_result

        mission_data = {
            "mission_id": "mission-456",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        result = await processor.process_aar(mission_data)

        assert isinstance(result, AARResult)
        assert result.mission_id == "mission-456"

        # Verify AAR was generated and stored
        mock_components["aar_generator"].generate_aar.assert_called_once_with(
            mission_data
        )
        mock_components["database"].store_aar.assert_called_once()
        mock_components["monitoring"].send_metric.assert_called()

    @pytest.mark.asyncio
    async def test_process_aar_error_handling(self, processor, mock_components):
        """Test AAR processing error handling"""
        await processor.initialize()

        # Configure mock to raise exception
        mock_components["aar_generator"].generate_aar.side_effect = Exception(
            "Test error"
        )

        mission_data = {
            "mission_id": "mission-456",
            "mission_type": "general",
            "data": {},
            "timestamp": datetime.now().isoformat(),
        }

        with pytest.raises(Exception, match="Test error"):
            await processor.process_aar(mission_data)

    @pytest.mark.asyncio
    async def test_check_compliance(self, processor, mock_components):
        """Test compliance checking"""
        await processor.initialize()

        # Configure mock
        mock_compliance_result = {
            "compliance_score": 0.88,
            "level": "good",
            "passed": True,
            "details": {"patterns": {"circle": 0.9}},
        }
        mock_components["compliance_checker"].check_compliance.return_value = (
            mock_compliance_result
        )

        test_data = {"performance": 0.9, "quality": 0.85}

        result = await processor.check_compliance(test_data)

        assert result == mock_compliance_result
        mock_components["compliance_checker"].check_compliance.assert_called_once_with(
            test_data
        )

    @pytest.mark.asyncio
    async def test_processor_shutdown(self, processor, mock_components):
        """Test processor shutdown"""
        await processor.initialize()
        await processor.shutdown()

        # Verify components were properly closed
        mock_components["database"].close.assert_called_once()
        mock_components["monitoring"].disconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_concurrent_aar_processing(self, processor, mock_components):
        """Test concurrent AAR processing"""
        await processor.initialize()

        # Configure mocks for concurrent processing
        def create_mock_result(mission_id):
            return AARResult(
                aar_id=f"aar-{mission_id}",
                mission_id=mission_id,
                compliance_score=0.85,
                report_content={"status": "success"},
                metadata={"version": "1.0"},
            )

        mock_components["aar_generator"].generate_aar.side_effect = (
            lambda data: create_mock_result(data["mission_id"])
        )

        # Create multiple mission data sets
        mission_data_list = []
        for i in range(3):
            mission_data_list.append(
                {
                    "mission_id": f"mission-{i}",
                    "mission_type": "general",
                    "data": {"index": i},
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Process concurrently
        tasks = [processor.process_aar(data) for data in mission_data_list]
        results = await asyncio.gather(*tasks)

        # Verify all processed successfully
        assert len(results) == 3
        for i, result in enumerate(results):
            assert result.mission_id == f"mission-{i}"

    @pytest.mark.asyncio
    async def test_metrics_collection(self, processor, mock_components):
        """Test metrics collection during processing"""
        await processor.initialize()

        # Configure mock
        mock_result = AARResult(
            aar_id="test-123",
            mission_id="mission-456",
            compliance_score=0.85,
            report_content={"status": "success"},
            metadata={"version": "1.0"},
        )
        mock_components["aar_generator"].generate_aar.return_value = mock_result

        mission_data = {
            "mission_id": "mission-456",
            "mission_type": "general",
            "data": {},
            "timestamp": datetime.now().isoformat(),
        }

        await processor.process_aar(mission_data)

        # Verify metrics were sent
        mock_components["monitoring"].send_metric.assert_called()

        # Check metrics include processing time and compliance score
        metric_calls = mock_components["monitoring"].send_metric.call_args_list
        assert len(metric_calls) > 0

    @pytest.mark.asyncio
    async def test_background_tasks(self, processor, mock_components):
        """Test background task execution"""
        await processor.initialize()

        # Test health monitoring background task
        await processor.start_background_monitoring()

        # Let it run briefly
        await asyncio.sleep(0.1)

        await processor.stop_background_monitoring()

        # Health checks should have been performed
        assert mock_components["database"].is_healthy.called
        assert mock_components["monitoring"].is_healthy.called

    @pytest.mark.asyncio
    async def test_error_recovery(self, processor, mock_components):
        """Test error recovery mechanisms"""
        await processor.initialize()

        # Simulate database failure
        mock_components["database"].is_healthy.return_value = False

        # Health check should detect the failure
        health_status = await processor.health_check()
        assert health_status["overall_health"] == "unhealthy"

        # Simulate recovery
        mock_components["database"].is_healthy.return_value = True

        # Health check should detect recovery
        health_status = await processor.health_check()
        assert health_status["overall_health"] == "healthy"

    @pytest.mark.asyncio
    async def test_configuration_validation(self, processor):
        """Test configuration validation"""
        # Test with invalid configuration
        with pytest.raises(ValueError):
            await processor.validate_configuration({"invalid": "config"})

        # Test with valid configuration
        valid_config = {
            "database_path": "/tmp/test.db",
            "monitoring_enabled": True,
            "compliance_threshold": 0.7,
        }

        result = await processor.validate_configuration(valid_config)
        assert result is True

    @pytest.mark.asyncio
    async def test_processor_state_management(self, processor):
        """Test processor state management"""
        # Initially not initialized
        assert not processor.is_initialized

        # After initialization
        await processor.initialize()
        assert processor.is_initialized

        # After shutdown
        await processor.shutdown()
        assert not processor.is_initialized


class TestAARProcessorIntegration:
    """Integration tests for AAR Processor"""

    @pytest.mark.asyncio
    async def test_end_to_end_processing(self):
        """Test end-to-end AAR processing"""
        # This test would use real components in a test environment
        # For now, it's a placeholder for full integration testing
        pass

    @pytest.mark.asyncio
    async def test_stress_testing(self):
        """Test processor under stress conditions"""
        # This test would simulate high load scenarios
        # For now, it's a placeholder for stress testing
        pass
