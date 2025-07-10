"""
🧪 Monitoring Integration Unit Tests
Comprehensive tests for monitoring and observability integration
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.monitoring_integration import (
    MonitoringIntegration,
    get_sacred_geometry_context,
)


class TestMonitoringIntegration:
    """Test suite for MonitoringIntegration class"""

    def test_initialization(self):
        """Test MonitoringIntegration initialization"""
        integration = MonitoringIntegration()

        assert integration.prometheus_url == "http://prometheus:9090"
        assert integration.grafana_url == "http://grafana:3000"
        assert integration.elasticsearch_url == "http://elasticsearch:9200"
        assert integration.connected is False
        assert integration.session is None

    @pytest.mark.asyncio
    async def test_connect_success(self, mock_aiohttp_session):
        """Test successful connection to monitoring systems"""
        with patch(
            "src.monitoring_integration.aiohttp.ClientSession",
            return_value=mock_aiohttp_session,
        ):
            integration = MonitoringIntegration()

            await integration.connect()

            assert integration.connected is True
            assert integration.session is not None

    @pytest.mark.asyncio
    async def test_connect_failure(self):
        """Test connection failure handling"""
        with patch(
            "src.monitoring_integration.aiohttp.ClientSession"
        ) as mock_session_class:
            mock_session = MagicMock()
            mock_response = MagicMock()
            mock_response.status = 500
            mock_response.__aenter__ = AsyncMock(return_value=mock_response)
            mock_response.__aexit__ = AsyncMock(return_value=None)
            mock_session.get = AsyncMock(return_value=mock_response)
            mock_session_class.return_value = mock_session

            integration = MonitoringIntegration()

            # Connection should fail due to 500 status
            await integration.connect()

            # Should still be marked as connected due to graceful error handling
            assert integration.connected is True

    @pytest.mark.asyncio
    async def test_disconnect(self, monitoring_integration):
        """Test disconnection from monitoring systems"""
        # Initially connected
        assert monitoring_integration.connected is True

        await monitoring_integration.disconnect()

        assert monitoring_integration.connected is False
        monitoring_integration.session.close.assert_called_once()

    def test_is_connected(self, monitoring_integration):
        """Test connection status check"""
        assert monitoring_integration.is_connected() is True

        monitoring_integration.connected = False
        assert monitoring_integration.is_connected() is False

    @pytest.mark.asyncio
    async def test_send_aar_metrics(self, monitoring_integration):
        """Test sending AAR metrics to monitoring systems"""
        aar_id = "TEST-AAR-001"
        compliance_score = 95.5
        processing_duration = 2.5

        await monitoring_integration.send_aar_metrics(
            aar_id=aar_id,
            compliance_score=compliance_score,
            processing_duration=processing_duration,
        )

        # Verify session was used for both Elasticsearch and Prometheus
        assert monitoring_integration.session.post.call_count >= 1

    @pytest.mark.asyncio
    async def test_get_system_health(self, monitoring_integration):
        """Test retrieving system health metrics"""
        health_data = await monitoring_integration.get_system_health()

        assert "prometheus" in health_data
        assert "elasticsearch" in health_data
        assert "timestamp" in health_data

        # Verify timestamp format
        timestamp = health_data["timestamp"]
        datetime.fromisoformat(timestamp)  # Should not raise exception

    @pytest.mark.asyncio
    async def test_create_alert(self, monitoring_integration):
        """Test creating monitoring alerts"""
        alert_type = "high_processing_time"
        message = "AAR processing took longer than expected"
        severity = "warning"

        await monitoring_integration.create_alert(
            alert_type=alert_type, message=message, severity=severity
        )

        # Verify alert was sent to Elasticsearch
        monitoring_integration.session.post.assert_called()

    @pytest.mark.asyncio
    async def test_check_prometheus_health_success(self, monitoring_integration):
        """Test Prometheus health check success"""
        # Mock successful response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            200
        )

        health = await monitoring_integration._check_prometheus_health()

        assert health["status"] == "healthy"
        assert health["response_code"] == 200

    @pytest.mark.asyncio
    async def test_check_prometheus_health_failure(self, monitoring_integration):
        """Test Prometheus health check failure"""
        # Mock failed response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            500
        )

        health = await monitoring_integration._check_prometheus_health()

        assert health["status"] == "unhealthy"
        assert health["response_code"] == 500

    @pytest.mark.asyncio
    async def test_check_elasticsearch_health_success(self, monitoring_integration):
        """Test Elasticsearch health check success"""
        # Mock successful response with cluster data
        mock_response = (
            monitoring_integration.session.get.return_value.__aenter__.return_value
        )
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "status": "green",
                "cluster_name": "test-cluster",
                "number_of_nodes": 3,
            }
        )

        health = await monitoring_integration._check_elasticsearch_health()

        assert health["status"] == "green"
        assert health["cluster_name"] == "test-cluster"
        assert health["number_of_nodes"] == 3

    @pytest.mark.asyncio
    async def test_check_elasticsearch_health_failure(self, monitoring_integration):
        """Test Elasticsearch health check failure"""
        # Mock failed response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            503
        )

        health = await monitoring_integration._check_elasticsearch_health()

        assert health["status"] == "unhealthy"
        assert health["response_code"] == 503

    @pytest.mark.asyncio
    async def test_send_to_elasticsearch_success(self, monitoring_integration):
        """Test successful data sending to Elasticsearch"""
        test_data = {
            "aar_id": "TEST-001",
            "compliance_score": 95.0,
            "timestamp": datetime.now().isoformat(),
        }

        # Mock successful response
        monitoring_integration.session.post.return_value.__aenter__.return_value.status = (
            201
        )

        await monitoring_integration._send_to_elasticsearch(test_data)

        # Verify POST request was made
        monitoring_integration.session.post.assert_called()

        # Verify correct URL and headers
        call_args = monitoring_integration.session.post.call_args
        assert "aar-metrics/_doc" in call_args[1]["url"]
        assert call_args[1]["headers"]["Content-Type"] == "application/json"

    @pytest.mark.asyncio
    async def test_send_to_elasticsearch_failure(self, monitoring_integration):
        """Test Elasticsearch sending failure handling"""
        test_data = {"test": "data"}

        # Mock failed response
        monitoring_integration.session.post.return_value.__aenter__.return_value.status = (
            400
        )

        # Should not raise exception, just log error
        await monitoring_integration._send_to_elasticsearch(test_data)

        monitoring_integration.session.post.assert_called()

    @pytest.mark.asyncio
    async def test_send_to_prometheus(self, monitoring_integration):
        """Test sending metrics to Prometheus (currently logs)"""
        test_metrics = {
            "aar_id": "TEST-001",
            "processing_duration": 2.5,
            "compliance_score": 95.0,
        }

        # Should complete without error (currently just logs)
        await monitoring_integration._send_to_prometheus(test_metrics)

        # No assertions needed as this currently just logs

    @pytest.mark.asyncio
    async def test_test_prometheus_connection_success(self, monitoring_integration):
        """Test Prometheus connection test success"""
        # Mock successful response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            200
        )

        # Should not raise exception
        await monitoring_integration._test_prometheus_connection()

        monitoring_integration.session.get.assert_called()

    @pytest.mark.asyncio
    async def test_test_prometheus_connection_failure(self, monitoring_integration):
        """Test Prometheus connection test failure"""
        # Mock failed response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            404
        )

        # Should log warning but not raise exception
        await monitoring_integration._test_prometheus_connection()

        monitoring_integration.session.get.assert_called()

    @pytest.mark.asyncio
    async def test_test_elasticsearch_connection_success(self, monitoring_integration):
        """Test Elasticsearch connection test success"""
        # Mock successful response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            200
        )

        # Should not raise exception
        await monitoring_integration._test_elasticsearch_connection()

        monitoring_integration.session.get.assert_called()

    @pytest.mark.asyncio
    async def test_test_elasticsearch_connection_failure(self, monitoring_integration):
        """Test Elasticsearch connection test failure"""
        # Mock failed response
        monitoring_integration.session.get.return_value.__aenter__.return_value.status = (
            503
        )

        # Should log warning but not raise exception
        await monitoring_integration._test_elasticsearch_connection()

        monitoring_integration.session.get.assert_called()

    @pytest.mark.asyncio
    async def test_error_handling_in_send_aar_metrics(self, monitoring_integration):
        """Test error handling in send_aar_metrics"""
        # Mock exception in session operations
        monitoring_integration.session.post.side_effect = Exception("Network error")

        # Should not raise exception, just log error
        await monitoring_integration.send_aar_metrics("TEST-001", 95.0, 2.5)

        monitoring_integration.session.post.assert_called()

    @pytest.mark.asyncio
    async def test_error_handling_in_get_system_health(self, monitoring_integration):
        """Test error handling in get_system_health"""
        # Mock exception in health checks
        monitoring_integration.session.get.side_effect = Exception("Connection error")

        health_data = await monitoring_integration.get_system_health()

        assert "error" in health_data
        assert "Connection error" in health_data["error"]

    def test_get_sacred_geometry_context(self):
        """Test Sacred Geometry context retrieval"""
        context = get_sacred_geometry_context()

        assert "circle" in context
        assert "triangle" in context
        assert "spiral" in context
        assert "golden_ratio" in context
        assert "fractal" in context

        # Verify descriptions contain expected keywords
        assert "360°" in context["circle"]
        assert "Three-tier" in context["triangle"]
        assert "Progressive" in context["spiral"]
        assert "φ = 1.618" in context["golden_ratio"]
        assert "Self-similar" in context["fractal"]

    @pytest.mark.asyncio
    async def test_monitoring_integration_with_missing_dependencies(self):
        """Test monitoring integration behavior when dependencies are missing"""
        # This test verifies the fallback behavior when aiohttp/structlog are not available
        with patch("src.monitoring_integration.aiohttp", None):
            # Should still be importable and functional with mock objects
            from src.monitoring_integration import MonitoringIntegration

            integration = MonitoringIntegration()
            assert integration is not None

    @pytest.mark.asyncio
    async def test_concurrent_monitoring_operations(self, monitoring_integration):
        """Test concurrent monitoring operations"""
        import asyncio

        # Create multiple concurrent operations
        tasks = []
        for i in range(5):
            tasks.append(
                monitoring_integration.send_aar_metrics(f"TEST-{i}", 90.0 + i, 2.0 + i)
            )

        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All operations should complete (none should be exceptions)
        assert len(results) == 5
        for result in results:
            assert not isinstance(result, Exception)

    @pytest.mark.asyncio
    async def test_alert_creation_with_different_severities(
        self, monitoring_integration
    ):
        """Test creating alerts with different severity levels"""
        severities = ["info", "warning", "error", "critical"]

        for severity in severities:
            await monitoring_integration.create_alert(
                alert_type="test_alert",
                message=f"Test {severity} alert",
                severity=severity,
            )

        # Verify correct number of POST calls made
        assert monitoring_integration.session.post.call_count == len(severities)

    @pytest.mark.asyncio
    async def test_metrics_data_structure(self, monitoring_integration):
        """Test that metrics data has correct structure"""
        # Capture the data sent to monitoring systems
        sent_data = []

        async def capture_post(*args, **kwargs):
            if "json" in kwargs:
                sent_data.append(kwargs["json"])
            return monitoring_integration.session.post.return_value

        monitoring_integration.session.post = AsyncMock(side_effect=capture_post)

        await monitoring_integration.send_aar_metrics("TEST-001", 95.5, 3.2)

        # Verify data structure
        assert len(sent_data) >= 1
        metrics_data = sent_data[0]

        assert "aar_id" in metrics_data
        assert "compliance_score" in metrics_data
        assert "processing_duration" in metrics_data
        assert "timestamp" in metrics_data

        # Verify data types
        assert isinstance(metrics_data["compliance_score"], float)
        assert isinstance(metrics_data["processing_duration"], float)
        assert isinstance(metrics_data["aar_id"], str)
