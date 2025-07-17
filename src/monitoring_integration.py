"""
Sacred Geometry AAR Processor - Monitoring Integration
"""

import json
from datetime import datetime
from typing import Any, Dict, Optional

try:
    import aiohttp
    import structlog

    logger = structlog.get_logger(__name__)
except ImportError:
    import logging

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    # Mock aiohttp for environments without it
    class MockClientSession:
        async def get(self, *args, **kwargs):
            class MockResponse:
                status = 200

                async def json(self):
                    return {}

                async def __aenter__(self):
                    return self

                async def __aexit__(self, *args):
                    pass

            return MockResponse()

        async def post(self, *args, **kwargs):
            class MockResponse:
                status = 200

                async def __aenter__(self):
                    return self

                async def __aexit__(self, *args):
                    pass

            return MockResponse()

        async def close(self):
            pass

    class aiohttp:
        ClientSession = MockClientSession


class MonitoringIntegration:
    """Integration with monitoring and observability systems"""

    def __init__(self):
        self.prometheus_url = "http://prometheus:9090"
        self.grafana_url = "http://grafana:3000"
        self.elasticsearch_url = "http://elasticsearch:9200"
        self.connected = False
        self.session: Optional[aiohttp.ClientSession] = None

    async def connect(self):
        """Connect to monitoring systems"""
        try:
            self.session = aiohttp.ClientSession()

            # Test connections
            await self._test_prometheus_connection()
            await self._test_elasticsearch_connection()

            self.connected = True
            logger.info("Connected to monitoring systems")

        except Exception as e:
            logger.error(f"Failed to connect to monitoring systems: {str(e)}")
            self.connected = False

    async def disconnect(self):
        """Disconnect from monitoring systems"""
        if self.session:
            await self.session.close()
        self.connected = False
        logger.info("Disconnected from monitoring systems")

    def is_connected(self) -> bool:
        """Check if connected to monitoring systems"""
        return self.connected

    async def send_aar_metrics(
        self, aar_id: str, compliance_score: float, processing_duration: float
    ):
        """Send AAR metrics to monitoring systems"""
        try:
            metrics = {
                "aar_id": aar_id,
                "compliance_score": compliance_score,
                "processing_duration": processing_duration,
                "timestamp": datetime.now().isoformat(),
            }

            await self._send_to_elasticsearch(metrics)
            await self._send_to_prometheus(metrics)

            logger.info(f"Sent metrics for AAR {aar_id}")

        except Exception as e:
            logger.error(f"Failed to send metrics: {str(e)}")

    async def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health metrics"""
        try:
            health_data = {
                "prometheus": await self._check_prometheus_health(),
                "elasticsearch": await self._check_elasticsearch_health(),
                "timestamp": datetime.now().isoformat(),
            }
            return health_data
        except Exception as e:
            logger.error(f"Failed to get system health: {str(e)}")
            return {"error": str(e)}

    async def _test_prometheus_connection(self):
        """Test connection to Prometheus"""
        url = f"{self.prometheus_url}/api/v1/query"
        params = {"query": "up"}

        async with self.session.get(url, params=params) as response:
            if response.status != 200:
                logger.warning(
                    f"Prometheus connection test returned: {response.status}"
                )

    async def _test_elasticsearch_connection(self):
        """Test connection to Elasticsearch"""
        url = f"{self.elasticsearch_url}/_cluster/health"

        async with self.session.get(url) as response:
            if response.status != 200:
                logger.warning(
                    f"Elasticsearch connection test returned: {response.status}"
                )

    async def _send_to_elasticsearch(self, data: Dict[str, Any]):
        """Send data to Elasticsearch"""
        url = f"{self.elasticsearch_url}/aar-metrics/_doc"
        headers = {"Content-Type": "application/json"}

        async with self.session.post(url, json=data, headers=headers) as response:
            if response.status not in [200, 201]:
                logger.error(f"Failed to send to Elasticsearch: {response.status}")

    async def _send_to_prometheus(self, metrics: Dict[str, Any]):
        """Send metrics to Prometheus"""
        logger.info(f"Prometheus metrics: {json.dumps(metrics, indent=2)}")

    async def _check_prometheus_health(self) -> Dict[str, Any]:
        """Check Prometheus health"""
        try:
            url = f"{self.prometheus_url}/-/healthy"
            async with self.session.get(url) as response:
                return {
                    "status": "healthy" if response.status == 200 else "unhealthy",
                    "response_code": response.status,
                }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def _check_elasticsearch_health(self) -> Dict[str, Any]:
        """Check Elasticsearch health"""
        try:
            url = f"{self.elasticsearch_url}/_cluster/health"
            async with self.session.get(url) as response:
                if response.status == 200:
                    health_data = await response.json()
                    return {
                        "status": health_data.get("status", "unknown"),
                        "cluster_name": health_data.get("cluster_name", "unknown"),
                        "number_of_nodes": health_data.get("number_of_nodes", 0),
                    }
                else:
                    return {"status": "unhealthy", "response_code": response.status}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    async def create_alert(
        self, alert_type: str, message: str, severity: str = "warning"
    ):
        """Create monitoring alert"""
        try:
            alert_data = {
                "alert_type": alert_type,
                "message": message,
                "severity": severity,
                "timestamp": datetime.now().isoformat(),
                "source": "aar-processor",
            }

            url = f"{self.elasticsearch_url}/alerts/_doc"
            headers = {"Content-Type": "application/json"}

            async with self.session.post(
                url, json=alert_data, headers=headers
            ) as response:
                if response.status in [200, 201]:
                    logger.info(f"Alert created: {alert_type} - {message}")
                else:
                    logger.error(f"Failed to create alert: {response.status}")

        except Exception as e:
            logger.error(f"Failed to create alert: {str(e)}")


def get_sacred_geometry_context():
    """Sacred Geometry monitoring patterns"""
    return {
        "circle": "Complete monitoring coverage - 360° observability",
        "triangle": "Three-tier monitoring - Infrastructure, Application, Business",
        "spiral": "Progressive monitoring enhancement with iterative improvement",
        "golden_ratio": "Optimal alert threshold ratios (φ = PHI)",
        "fractal": "Self-similar monitoring patterns at all scales",
    }
