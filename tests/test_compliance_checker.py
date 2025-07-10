#!/usr/bin/env python3
"""
🧪 Compliance Checker Unit Tests
Comprehensive testing for the Sacred Geometry compliance monitoring system
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.compliance_checker import ComplianceChecker
from src.sacred_geometry_engine import SacredGeometryEngine


class TestComplianceChecker:
    """Test Compliance Checker functionality"""

    @pytest.fixture
    def mock_sacred_geometry(self):
        """Mock Sacred Geometry engine"""
        engine = MagicMock(spec=SacredGeometryEngine)
        engine.calculate_compliance = AsyncMock(return_value=0.85)
        engine.validate_pattern = AsyncMock(return_value=True)
        engine.get_geometry_insights = AsyncMock(
            return_value={
                "patterns": {
                    "circle": 0.9,
                    "triangle": 0.85,
                    "spiral": 0.8,
                    "golden_ratio": 0.88,
                    "fractal": 0.82,
                },
                "overall_score": 0.85,
            }
        )
        return engine

    @pytest.fixture
    def compliance_checker(self, mock_sacred_geometry):
        """Create Compliance Checker instance"""
        return ComplianceChecker(mock_sacred_geometry)

    def test_compliance_checker_initialization(self, mock_sacred_geometry):
        """Test compliance checker initialization"""
        checker = ComplianceChecker(mock_sacred_geometry)

        assert checker.sacred_geometry == mock_sacred_geometry
        assert isinstance(checker.compliance_thresholds, dict)

        # Verify threshold structure
        expected_thresholds = [
            "excellent",
            "good",
            "acceptable",
            "needs_improvement",
            "critical",
        ]
        for threshold in expected_thresholds:
            assert threshold in checker.compliance_thresholds
            assert isinstance(checker.compliance_thresholds[threshold], (int, float))

        # Verify thresholds are in descending order
        thresholds = list(checker.compliance_thresholds.values())
        assert thresholds == sorted(thresholds, reverse=True)

        assert checker.current_compliance == 0.0
        assert checker.last_check is None

    def test_compliance_thresholds_values(self, compliance_checker):
        """Test compliance threshold values are reasonable"""
        thresholds = compliance_checker.compliance_thresholds

        assert thresholds["excellent"] == 0.9
        assert thresholds["good"] == 0.8
        assert thresholds["acceptable"] == 0.7
        assert thresholds["needs_improvement"] == 0.5
        assert thresholds["critical"] == 0.3

        # Ensure all thresholds are between 0 and 1
        for threshold_value in thresholds.values():
            assert 0.0 <= threshold_value <= 1.0

    @pytest.mark.asyncio
    async def test_get_current_compliance(self, compliance_checker):
        """Test getting current compliance level"""
        # Initial compliance should be 0.0
        compliance = await compliance_checker.get_current_compliance()
        assert compliance == 0.0

        # Update compliance and verify
        await compliance_checker.update_compliance(0.75)
        compliance = await compliance_checker.get_current_compliance()
        assert compliance == 0.75

    @pytest.mark.asyncio
    async def test_update_compliance(self, compliance_checker):
        """Test updating compliance score"""
        new_score = 0.88
        before_update = datetime.now()

        await compliance_checker.update_compliance(new_score)

        after_update = datetime.now()

        assert compliance_checker.current_compliance == new_score
        assert compliance_checker.last_check is not None
        assert before_update <= compliance_checker.last_check <= after_update

    @pytest.mark.asyncio
    async def test_update_compliance_boundary_values(self, compliance_checker):
        """Test updating compliance with boundary values"""
        # Test minimum value
        await compliance_checker.update_compliance(0.0)
        assert compliance_checker.current_compliance == 0.0

        # Test maximum value
        await compliance_checker.update_compliance(1.0)
        assert compliance_checker.current_compliance == 1.0

    @pytest.mark.asyncio
    async def test_get_detailed_compliance(self, compliance_checker):
        """Test getting detailed compliance information"""
        # Set up initial compliance
        await compliance_checker.update_compliance(0.82)

        detailed_compliance = await compliance_checker.get_detailed_compliance()

        assert isinstance(detailed_compliance, dict)
        assert "current_score" in detailed_compliance
        assert "level" in detailed_compliance
        assert "last_check" in detailed_compliance
        assert "thresholds" in detailed_compliance
        assert "recommendations" in detailed_compliance

        assert detailed_compliance["current_score"] == 0.82
        assert detailed_compliance["level"] == "good"  # 0.82 is in "good" range
        assert isinstance(detailed_compliance["last_check"], datetime)

    @pytest.mark.asyncio
    async def test_compliance_level_classification(self, compliance_checker):
        """Test compliance level classification for different scores"""
        test_cases = [
            (0.95, "excellent"),
            (0.85, "good"),
            (0.75, "acceptable"),
            (0.55, "needs_improvement"),
            (0.25, "critical"),
            (0.0, "critical"),
        ]

        for score, expected_level in test_cases:
            await compliance_checker.update_compliance(score)
            detailed = await compliance_checker.get_detailed_compliance()
            assert detailed["level"] == expected_level

    @pytest.mark.asyncio
    async def test_check_compliance_with_data(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test compliance checking with actual data"""
        test_data = {
            "performance_metrics": {
                "success_rate": 0.95,
                "error_rate": 0.05,
                "response_time": 100,
            },
            "quality_metrics": {
                "accuracy": 0.92,
                "precision": 0.89,
                "completeness": 0.96,
            },
        }

        # Configure mock to return specific compliance score
        mock_sacred_geometry.calculate_compliance.return_value = 0.87

        result = await compliance_checker.check_compliance(test_data)

        # Verify Sacred Geometry engine was called
        mock_sacred_geometry.calculate_compliance.assert_called_once_with(test_data)

        # Verify result structure
        assert isinstance(result, dict)
        assert "compliance_score" in result
        assert "level" in result
        assert "passed" in result
        assert "details" in result

        assert result["compliance_score"] == 0.87
        assert result["level"] == "good"
        assert result["passed"] is True

    @pytest.mark.asyncio
    async def test_check_compliance_failure(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test compliance checking with failing data"""
        test_data = {
            "performance_metrics": {
                "success_rate": 0.3,
                "error_rate": 0.7,
                "response_time": 5000,
            }
        }

        # Configure mock to return low compliance score
        mock_sacred_geometry.calculate_compliance.return_value = 0.25

        result = await compliance_checker.check_compliance(test_data)

        assert result["compliance_score"] == 0.25
        assert result["level"] == "critical"
        assert result["passed"] is False

    @pytest.mark.asyncio
    async def test_generate_compliance_report(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test compliance report generation"""
        # Set up some compliance history
        await compliance_checker.update_compliance(0.85)

        test_data = {
            "mission_id": "test-mission-123",
            "metrics": {"performance": 0.9, "quality": 0.8},
        }

        report = await compliance_checker.generate_compliance_report(test_data)

        assert isinstance(report, dict)
        assert "mission_id" in report
        assert "compliance_score" in report
        assert "level" in report
        assert "timestamp" in report
        assert "details" in report
        assert "recommendations" in report

        assert report["mission_id"] == "test-mission-123"
        assert isinstance(report["timestamp"], datetime)

    @pytest.mark.asyncio
    async def test_compliance_history_tracking(self, compliance_checker):
        """Test compliance history tracking"""
        scores = [0.5, 0.7, 0.85, 0.9, 0.88]

        for score in scores:
            await compliance_checker.update_compliance(score)

        history = await compliance_checker.get_compliance_history()

        assert isinstance(history, list)
        assert len(history) <= 10  # Should maintain reasonable history size

        # Verify most recent score is last
        assert history[-1]["score"] == 0.88

    @pytest.mark.asyncio
    async def test_compliance_trend_analysis(self, compliance_checker):
        """Test compliance trend analysis"""
        # Simulate improving trend
        improving_scores = [0.5, 0.6, 0.7, 0.8, 0.85]

        for score in improving_scores:
            await compliance_checker.update_compliance(score)

        trend = await compliance_checker.analyze_compliance_trend()

        assert isinstance(trend, dict)
        assert "direction" in trend
        assert "magnitude" in trend
        assert "confidence" in trend

        assert trend["direction"] == "improving"
        assert trend["magnitude"] > 0

    @pytest.mark.asyncio
    async def test_compliance_alerts(self, compliance_checker):
        """Test compliance alerting system"""
        # Test critical compliance alert
        await compliance_checker.update_compliance(0.2)  # Critical level

        alerts = await compliance_checker.get_compliance_alerts()

        assert isinstance(alerts, list)
        assert len(alerts) > 0

        critical_alert = alerts[0]
        assert critical_alert["level"] == "critical"
        assert critical_alert["score"] == 0.2
        assert "message" in critical_alert

    @pytest.mark.asyncio
    async def test_compliance_recommendations(self, compliance_checker):
        """Test compliance recommendations generation"""
        test_data = {
            "performance": 0.6,  # Below good threshold
            "quality": 0.9,  # Good
            "efficiency": 0.4,  # Poor
        }

        recommendations = await compliance_checker.get_compliance_recommendations(
            test_data
        )

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

        # Should have recommendations for improving performance and efficiency
        rec_text = " ".join([rec["description"] for rec in recommendations])
        assert "performance" in rec_text.lower() or "efficiency" in rec_text.lower()

    @pytest.mark.asyncio
    async def test_compliance_monitoring_continuous(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test continuous compliance monitoring"""
        import asyncio

        # Start monitoring
        monitoring_task = asyncio.create_task(
            compliance_checker.start_continuous_monitoring(interval=0.1)
        )

        # Let it run briefly
        await asyncio.sleep(0.3)

        # Stop monitoring
        monitoring_task.cancel()

        try:
            await monitoring_task
        except asyncio.CancelledError:
            pass

        # Verify monitoring was active
        assert compliance_checker.last_check is not None

    @pytest.mark.asyncio
    async def test_sacred_geometry_integration(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test Sacred Geometry engine integration"""
        test_data = {"test": "data"}

        await compliance_checker.check_compliance(test_data)

        # Verify Sacred Geometry methods were called
        mock_sacred_geometry.calculate_compliance.assert_called_once_with(test_data)

    @pytest.mark.asyncio
    async def test_compliance_error_handling(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test error handling in compliance checking"""
        # Configure mock to raise exception
        mock_sacred_geometry.calculate_compliance.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            await compliance_checker.check_compliance({"test": "data"})

    @pytest.mark.asyncio
    async def test_compliance_data_validation(self, compliance_checker):
        """Test validation of compliance data input"""
        # Test with None data
        with pytest.raises(ValueError):
            await compliance_checker.check_compliance(None)

        # Test with empty data
        result = await compliance_checker.check_compliance({})
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_compliance_threshold_customization(self, compliance_checker):
        """Test customization of compliance thresholds"""
        custom_thresholds = {
            "excellent": 0.95,
            "good": 0.85,
            "acceptable": 0.75,
            "needs_improvement": 0.55,
            "critical": 0.35,
        }

        compliance_checker.update_thresholds(custom_thresholds)

        # Test classification with new thresholds
        await compliance_checker.update_compliance(0.8)
        detailed = await compliance_checker.get_detailed_compliance()

        # With new thresholds, 0.8 should be "acceptable" not "good"
        assert detailed["level"] == "acceptable"

    @pytest.mark.asyncio
    async def test_concurrent_compliance_checks(
        self, compliance_checker, mock_sacred_geometry
    ):
        """Test concurrent compliance checking"""
        import asyncio

        test_datasets = [{"id": i, "performance": 0.8 + (i * 0.02)} for i in range(5)]

        # Configure mock to return different scores
        mock_sacred_geometry.calculate_compliance.side_effect = [
            0.8,
            0.82,
            0.84,
            0.86,
            0.88,
        ]

        # Check compliance concurrently
        tasks = [compliance_checker.check_compliance(data) for data in test_datasets]
        results = await asyncio.gather(*tasks)

        # Verify all results are valid
        assert len(results) == 5
        for i, result in enumerate(results):
            assert isinstance(result, dict)
            assert "compliance_score" in result
            assert result["compliance_score"] == 0.8 + (i * 0.02)

    def test_compliance_level_method(self, compliance_checker):
        """Test private compliance level determination method"""
        # Test boundary conditions
        assert compliance_checker._get_compliance_level(1.0) == "excellent"
        assert compliance_checker._get_compliance_level(0.9) == "excellent"
        assert compliance_checker._get_compliance_level(0.89) == "good"
        assert compliance_checker._get_compliance_level(0.8) == "good"
        assert compliance_checker._get_compliance_level(0.79) == "acceptable"
        assert compliance_checker._get_compliance_level(0.7) == "acceptable"
        assert compliance_checker._get_compliance_level(0.69) == "needs_improvement"
        assert compliance_checker._get_compliance_level(0.5) == "needs_improvement"
        assert compliance_checker._get_compliance_level(0.49) == "critical"
        assert compliance_checker._get_compliance_level(0.0) == "critical"
