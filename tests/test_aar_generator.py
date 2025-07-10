#!/usr/bin/env python3
"""
🧪 AAR Generator Unit Tests
Comprehensive testing for the AAR generation system
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.aar_generator import AARGenerator, AARResult
from src.sacred_geometry_engine import SacredGeometryEngine


class TestAARResult:
    """Test AAR result container"""

    def test_aar_result_creation(self):
        """Test AAR result object creation"""
        aar_id = "test-aar-123"
        mission_id = "mission-456"
        compliance_score = 0.85
        report_content = {"status": "success", "insights": ["test insight"]}
        metadata = {"version": "1.0", "type": "test"}

        result = AARResult(
            aar_id=aar_id,
            mission_id=mission_id,
            compliance_score=compliance_score,
            report_content=report_content,
            metadata=metadata,
        )

        assert result.aar_id == aar_id
        assert result.mission_id == mission_id
        assert result.compliance_score == compliance_score
        assert result.report_content == report_content
        assert result.metadata == metadata
        assert isinstance(result.generated_at, datetime)

    def test_aar_result_timestamp(self):
        """Test AAR result includes valid timestamp"""
        before = datetime.now()
        result = AARResult("test", "mission", 0.8, {}, {})
        after = datetime.now()

        assert before <= result.generated_at <= after


class TestAARGenerator:
    """Test AAR generation functionality"""

    @pytest.fixture
    def mock_sacred_geometry(self):
        """Mock Sacred Geometry engine"""
        engine = MagicMock(spec=SacredGeometryEngine)
        engine.validate_pattern = AsyncMock(return_value=True)
        engine.calculate_compliance = AsyncMock(return_value=0.85)
        engine.get_geometry_insights = AsyncMock(
            return_value={
                "patterns": ["circle", "triangle"],
                "balance": 0.9,
                "efficiency": 0.8,
            }
        )
        return engine

    @pytest.fixture
    def aar_generator(self, mock_sacred_geometry):
        """Create AAR generator instance"""
        return AARGenerator(mock_sacred_geometry)

    def test_aar_generator_initialization(self, mock_sacred_geometry):
        """Test AAR generator initialization"""
        generator = AARGenerator(mock_sacred_geometry)

        assert generator.sacred_geometry == mock_sacred_geometry
        assert isinstance(generator.report_templates, dict)
        assert "file_organization" in generator.report_templates
        assert "monitoring_system" in generator.report_templates
        assert "development" in generator.report_templates
        assert "deployment" in generator.report_templates
        assert "maintenance" in generator.report_templates
        assert "general" in generator.report_templates

    @pytest.mark.asyncio
    async def test_generate_aar_success(self, aar_generator):
        """Test successful AAR generation"""
        mission_data = {
            "mission_id": "test-mission-123",
            "mission_type": "file_organization",
            "data": {"files_processed": 100, "errors": 2, "warnings": 5},
            "timestamp": datetime.now().isoformat(),
        }

        result = await aar_generator.generate_aar(mission_data)

        assert isinstance(result, AARResult)
        assert result.mission_id == "test-mission-123"
        assert 0.0 <= result.compliance_score <= 1.0
        assert isinstance(result.report_content, dict)
        assert isinstance(result.metadata, dict)

    @pytest.mark.asyncio
    async def test_generate_aar_invalid_mission_type(self, aar_generator):
        """Test AAR generation with invalid mission type"""
        mission_data = {
            "mission_id": "test-mission-123",
            "mission_type": "invalid_type",
            "data": {},
            "timestamp": datetime.now().isoformat(),
        }

        with pytest.raises(ValueError, match="Unknown mission type"):
            await aar_generator.generate_aar(mission_data)

    @pytest.mark.asyncio
    async def test_generate_aar_missing_mission_id(self, aar_generator):
        """Test AAR generation with missing mission ID"""
        mission_data = {
            "mission_type": "file_organization",
            "data": {},
            "timestamp": datetime.now().isoformat(),
        }

        with pytest.raises(KeyError):
            await aar_generator.generate_aar(mission_data)

    @pytest.mark.asyncio
    async def test_generate_aar_all_mission_types(self, aar_generator):
        """Test AAR generation for all supported mission types"""
        mission_types = [
            "file_organization",
            "monitoring_system",
            "development",
            "deployment",
            "maintenance",
            "general",
        ]

        for mission_type in mission_types:
            mission_data = {
                "mission_id": f"test-{mission_type}-123",
                "mission_type": mission_type,
                "data": {"test": "data"},
                "timestamp": datetime.now().isoformat(),
            }

            result = await aar_generator.generate_aar(mission_data)

            assert isinstance(result, AARResult)
            assert result.mission_id == f"test-{mission_type}-123"
            assert mission_type in result.metadata.get("mission_type", "")

    @pytest.mark.asyncio
    async def test_file_organization_aar_generation(self, aar_generator):
        """Test file organization specific AAR generation"""
        mission_data = {
            "mission_id": "file-org-123",
            "mission_type": "file_organization",
            "data": {
                "files_processed": 150,
                "files_organized": 145,
                "errors": 3,
                "warnings": 8,
                "duration": 300,
                "patterns_detected": ["duplicate", "naming_convention"],
            },
            "timestamp": datetime.now().isoformat(),
        }

        result = await aar_generator.generate_aar(mission_data)

        assert result.mission_id == "file-org-123"
        assert "file_organization" in result.report_content
        assert "success_rate" in result.report_content["file_organization"]
        assert "performance_metrics" in result.report_content["file_organization"]

    @pytest.mark.asyncio
    async def test_monitoring_system_aar_generation(self, aar_generator):
        """Test monitoring system specific AAR generation"""
        mission_data = {
            "mission_id": "monitoring-123",
            "mission_type": "monitoring_system",
            "data": {
                "metrics_collected": 1000,
                "alerts_triggered": 5,
                "system_health": 0.95,
                "response_time": 50,
                "uptime": 0.999,
            },
            "timestamp": datetime.now().isoformat(),
        }

        result = await aar_generator.generate_aar(mission_data)

        assert result.mission_id == "monitoring-123"
        assert "monitoring_system" in result.report_content
        assert "health_score" in result.report_content["monitoring_system"]
        assert "alert_analysis" in result.report_content["monitoring_system"]

    @pytest.mark.asyncio
    async def test_development_aar_generation(self, aar_generator):
        """Test development specific AAR generation"""
        mission_data = {
            "mission_id": "dev-123",
            "mission_type": "development",
            "data": {
                "code_lines": 500,
                "tests_written": 50,
                "test_coverage": 0.85,
                "bugs_fixed": 8,
                "features_added": 3,
            },
            "timestamp": datetime.now().isoformat(),
        }

        result = await aar_generator.generate_aar(mission_data)

        assert result.mission_id == "dev-123"
        assert "development" in result.report_content
        assert "quality_metrics" in result.report_content["development"]
        assert "productivity_analysis" in result.report_content["development"]

    @pytest.mark.asyncio
    async def test_sacred_geometry_integration(
        self, aar_generator, mock_sacred_geometry
    ):
        """Test Sacred Geometry engine integration"""
        mission_data = {
            "mission_id": "geometry-test-123",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        # Configure mock to return specific values
        mock_sacred_geometry.validate_pattern.return_value = True
        mock_sacred_geometry.calculate_compliance.return_value = 0.92
        mock_sacred_geometry.get_geometry_insights.return_value = {
            "circle_completeness": 0.9,
            "triangle_stability": 0.95,
            "spiral_growth": 0.88,
            "golden_ratio_balance": 0.91,
            "fractal_complexity": 0.87,
        }

        result = await aar_generator.generate_aar(mission_data)

        # Verify Sacred Geometry methods were called
        mock_sacred_geometry.validate_pattern.assert_called()
        mock_sacred_geometry.calculate_compliance.assert_called()
        mock_sacred_geometry.get_geometry_insights.assert_called()

        # Verify compliance score reflects Sacred Geometry calculation
        assert result.compliance_score == 0.92
        assert "sacred_geometry" in result.metadata

    @pytest.mark.asyncio
    async def test_aar_generation_error_handling(
        self, aar_generator, mock_sacred_geometry
    ):
        """Test error handling during AAR generation"""
        mission_data = {
            "mission_id": "error-test-123",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        # Configure mock to raise exception
        mock_sacred_geometry.calculate_compliance.side_effect = Exception("Test error")

        with pytest.raises(Exception, match="Test error"):
            await aar_generator.generate_aar(mission_data)

    @pytest.mark.asyncio
    async def test_concurrent_aar_generation(self, aar_generator):
        """Test concurrent AAR generation"""
        import asyncio

        mission_data_list = []
        for i in range(5):
            mission_data_list.append(
                {
                    "mission_id": f"concurrent-test-{i}",
                    "mission_type": "general",
                    "data": {"index": i},
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Generate AARs concurrently
        tasks = [
            aar_generator.generate_aar(mission_data)
            for mission_data in mission_data_list
        ]
        results = await asyncio.gather(*tasks)

        # Verify all results are unique and valid
        assert len(results) == 5
        mission_ids = [result.mission_id for result in results]
        assert len(set(mission_ids)) == 5  # All unique

        for i, result in enumerate(results):
            assert result.mission_id == f"concurrent-test-{i}"
            assert isinstance(result, AARResult)

    def test_report_template_structure(self, aar_generator):
        """Test report template structure and availability"""
        templates = aar_generator.report_templates

        # Verify all expected templates exist
        expected_templates = [
            "file_organization",
            "monitoring_system",
            "development",
            "deployment",
            "maintenance",
            "general",
        ]

        for template in expected_templates:
            assert template in templates
            assert callable(templates[template])

    @pytest.mark.asyncio
    async def test_aar_metadata_completeness(self, aar_generator):
        """Test AAR metadata includes all required fields"""
        mission_data = {
            "mission_id": "metadata-test-123",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        result = await aar_generator.generate_aar(mission_data)

        # Verify metadata structure
        metadata = result.metadata
        assert "generator_version" in metadata
        assert "processing_time" in metadata
        assert "sacred_geometry" in metadata
        assert "mission_type" in metadata
        assert isinstance(metadata["processing_time"], (int, float))

    @pytest.mark.asyncio
    async def test_compliance_score_validation(self, aar_generator):
        """Test compliance score is always within valid range"""
        mission_data = {
            "mission_id": "compliance-test-123",
            "mission_type": "general",
            "data": {"test": "data"},
            "timestamp": datetime.now().isoformat(),
        }

        # Test multiple generations to ensure consistency
        for _ in range(10):
            result = await aar_generator.generate_aar(mission_data)
            assert 0.0 <= result.compliance_score <= 1.0
            assert isinstance(result.compliance_score, (int, float))
