"""
🧪 Monitoring Integration Unit Tests - Fixed Version
Tests that match the actual MonitoringIntegration API
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.monitoring_integration import (
    MonitoringIntegration,
    get_sacred_geometry_context,
)


class TestMonitoringIntegrationFixed:
    """Test suite for MonitoringIntegration class - matches real API"""

    def test_initialization(self):
        """Test MonitoringIntegration initialization"""
        integration = MonitoringIntegration()

        assert integration.prometheus_url == "http://prometheus:9090"
        assert integration.grafana_url == "http://grafana:3000"
        assert integration.elasticsearch_url == "http://elasticsearch:9200"
        assert integration.connected is False
        assert integration.session is None

    def test_is_connected_initial_state(self):
        """Test is_connected returns False initially"""
        integration = MonitoringIntegration()
        assert integration.is_connected() is False @ pytest.mark.asyncio

    async def test_connect_success(self):
        """Test successful connection to monitoring systems"""
        with patch(
            "src.monitoring_integration.aiohttp.ClientSession"
        ) as mock_session_class:
            # Mock the session and responses
            mock_session = MagicMock()
            mock_response = MagicMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={"status": "ready"})

            # Create a proper async context manager
            async def mock_get(*args, **kwargs):
                return mock_response

            mock_session.get = mock_get
            mock_session_class.return_value = mock_session

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
            # Mock session that raises exception
            mock_session = MagicMock()
            mock_session.get = AsyncMock(side_effect=Exception("Connection failed"))
            mock_session_class.return_value = mock_session

            integration = MonitoringIntegration()
            await integration.connect()

            assert integration.connected is False

    @pytest.mark.asyncio
    async def test_disconnect(self):
        """Test disconnect from monitoring systems"""
        integration = MonitoringIntegration()

        # Mock a connected session
        mock_session = MagicMock()
        mock_session.close = AsyncMock()
        integration.session = mock_session
        integration.connected = True

        await integration.disconnect()

        assert integration.connected is False
        mock_session.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_aar_metrics(self):
        """Test sending AAR metrics to monitoring systems"""
        integration = MonitoringIntegration()

        # Mock connected state
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.post = AsyncMock(return_value=mock_response)
        integration.session = mock_session
        integration.connected = True

        await integration.send_aar_metrics("test-aar-123", 0.95, 2.5)

        # Verify metrics were sent
        assert mock_session.post.called

    @pytest.mark.asyncio
    async def test_get_system_health(self):
        """Test getting system health status"""
        integration = MonitoringIntegration()

        # Mock connected state with health responses
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"status": "healthy"})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.get = AsyncMock(return_value=mock_response)
        integration.session = mock_session
        integration.connected = True

        health = await integration.get_system_health()

        assert isinstance(health, dict)
        assert "prometheus" in health
        assert "elasticsearch" in health

    @pytest.mark.asyncio
    async def test_create_alert(self):
        """Test creating monitoring alerts"""
        integration = MonitoringIntegration()

        # Mock connected state
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.post = AsyncMock(return_value=mock_response)
        integration.session = mock_session
        integration.connected = True

        await integration.create_alert(
            title="Test Alert", message="Test alert message", severity="warning"
        )

        # Verify alert was created
        assert mock_session.post.called

    def test_get_sacred_geometry_context(self):
        """Test Sacred Geometry context function"""
        context = get_sacred_geometry_context()

        assert isinstance(context, dict)
        assert "circle" in context
        assert "triangle" in context
        assert "spiral" in context
        assert "golden_ratio" in context
        assert "fractal" in context

        # Verify content contains expected patterns
        assert "360°" in context["circle"]
        assert "Three-tier" in context["triangle"]
        assert "φ = 1.618" in context["golden_ratio"]

    @pytest.mark.asyncio
    async def test_private_method_prometheus_health(self):
        """Test private method for Prometheus health check"""
        integration = MonitoringIntegration()

        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"status": "ready"})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.get = AsyncMock(return_value=mock_response)
        integration.session = mock_session

        health = await integration._check_prometheus_health()

        assert isinstance(health, dict)
        assert health["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_private_method_elasticsearch_health(self):
        """Test private method for Elasticsearch health check"""
        integration = MonitoringIntegration()

        # Mock session
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"status": "green"})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.get = AsyncMock(return_value=mock_response)
        integration.session = mock_session

        health = await integration._check_elasticsearch_health()

        assert isinstance(health, dict)
        assert health["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_monitoring_integration_with_mock_fallback(self):
        """Test that monitoring works even when aiohttp is not available"""
        # This tests the MockClientSession fallback
        with patch("src.monitoring_integration.aiohttp", None):
            # This should use the mock fallback
            integration = MonitoringIntegration()
            await integration.connect()

            # Even with mock, basic operations should work
            await integration.send_aar_metrics("mock-test", 1.0, 1.0)
            health = await integration.get_system_health()
            assert isinstance(health, dict)
