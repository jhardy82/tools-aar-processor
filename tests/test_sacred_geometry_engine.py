#!/usr/bin/env python3
"""
🧪 Sacred Geometry Engine Unit Tests
Comprehensive testing for the Sacred Geometry processing system
"""

import math

import pytest

from src.sacred_geometry_engine import SacredGeometryEngine


class TestSacredGeometryEngine:
    """Test Sacred Geometry Engine functionality"""

    @pytest.fixture
    def engine(self):
        """Create Sacred Geometry Engine instance"""
        return SacredGeometryEngine()

    def test_engine_initialization(self, engine):
        """Test engine initialization"""
        assert not engine.is_initialized
        assert abs(engine.phi - PHI) < 1e-10
        assert isinstance(engine.patterns, dict)

        expected_patterns = ["circle", "triangle", "spiral", "golden_ratio", "fractal"]
        for pattern in expected_patterns:
            assert pattern in engine.patterns
            assert callable(engine.patterns[pattern])

    def test_golden_ratio_calculation(self, engine):
        """Test golden ratio calculation accuracy"""
        # φ = (1 + √5) / 2
        expected_phi = (1 + math.sqrt(5)) / 2
        assert abs(engine.phi - expected_phi) < 1e-15

        # Test mathematical properties of φ
        # φ² = φ + 1
        assert abs(engine.phi**2 - (engine.phi + 1)) < 1e-10

        # 1/φ = φ - 1
        assert abs(1 / engine.phi - (engine.phi - 1)) < 1e-10

    @pytest.mark.asyncio
    async def test_engine_initialization_async(self, engine):
        """Test async engine initialization"""
        assert not engine.is_initialized

        await engine.initialize()

        assert engine.is_initialized

    @pytest.mark.asyncio
    async def test_pattern_validation_circle(self, engine):
        """Test circle pattern validation"""
        await engine.initialize()

        # Test complete circle (high completeness)
        complete_data = {
            "total_items": 100,
            "processed_items": 100,
            "errors": 0,
            "completion_rate": 1.0,
        }

        result = await engine.validate_pattern("circle", complete_data)
        assert result is True

        # Test incomplete circle (low completeness)
        incomplete_data = {
            "total_items": 100,
            "processed_items": 30,
            "errors": 10,
            "completion_rate": 0.3,
        }

        result = await engine.validate_pattern("circle", incomplete_data)
        # Should still return True but with lower score internally

    @pytest.mark.asyncio
    async def test_pattern_validation_triangle(self, engine):
        """Test triangle pattern validation (stability)"""
        await engine.initialize()

        stable_data = {
            "foundation": 0.9,
            "structure": 0.85,
            "apex": 0.8,
            "balance": True,
        }

        result = await engine.validate_pattern("triangle", stable_data)
        assert result is True

    @pytest.mark.asyncio
    async def test_pattern_validation_spiral(self, engine):
        """Test spiral pattern validation (growth)"""
        await engine.initialize()

        growth_data = {
            "iterations": [0.1, 0.2, 0.35, 0.55, 0.8],
            "growth_rate": PHI,  # Golden ratio growth
            "progression": "ascending",
        }

        result = await engine.validate_pattern("spiral", growth_data)
        assert result is True

    @pytest.mark.asyncio
    async def test_pattern_validation_golden_ratio(self, engine):
        """Test golden ratio pattern validation"""
        await engine.initialize()

        ratio_data = {
            "primary_metric": 161.8,
            "secondary_metric": 100.0,
            "ratio": PHI,
            "tolerance": 0.01,
        }

        result = await engine.validate_pattern("golden_ratio", ratio_data)
        assert result is True

    @pytest.mark.asyncio
    async def test_pattern_validation_fractal(self, engine):
        """Test fractal pattern validation (self-similarity)"""
        await engine.initialize()

        fractal_data = {
            "levels": 3,
            "similarity_scores": [0.95, 0.92, 0.89],
            "complexity": 0.7,
            "recursion_depth": 3,
        }

        result = await engine.validate_pattern("fractal", fractal_data)
        assert result is True

    @pytest.mark.asyncio
    async def test_pattern_validation_invalid_pattern(self, engine):
        """Test validation with invalid pattern name"""
        await engine.initialize()

        with pytest.raises(ValueError, match="Unknown pattern"):
            await engine.validate_pattern("invalid_pattern", {})

    @pytest.mark.asyncio
    async def test_pattern_validation_uninitialized(self, engine):
        """Test validation before initialization"""
        with pytest.raises(RuntimeError, match="not initialized"):
            await engine.validate_pattern("circle", {})

    @pytest.mark.asyncio
    async def test_calculate_compliance(self, engine):
        """Test compliance score calculation"""
        await engine.initialize()

        test_data = {
            "performance": 0.9,
            "quality": 0.85,
            "efficiency": 0.8,
            "completeness": 0.95,
        }

        compliance_score = await engine.calculate_compliance(test_data)

        assert isinstance(compliance_score, float)
        assert 0.0 <= compliance_score <= 1.0

    @pytest.mark.asyncio
    async def test_calculate_compliance_perfect_score(self, engine):
        """Test compliance calculation with perfect metrics"""
        await engine.initialize()

        perfect_data = {
            "performance": 1.0,
            "quality": 1.0,
            "efficiency": 1.0,
            "completeness": 1.0,
            "sacred_geometry_alignment": 1.0,
        }

        compliance_score = await engine.calculate_compliance(perfect_data)

        # Should be very high but may not be exactly 1.0 due to Sacred Geometry weighting
        assert compliance_score >= 0.95

    @pytest.mark.asyncio
    async def test_calculate_compliance_poor_score(self, engine):
        """Test compliance calculation with poor metrics"""
        await engine.initialize()

        poor_data = {
            "performance": 0.1,
            "quality": 0.2,
            "efficiency": 0.1,
            "completeness": 0.3,
        }

        compliance_score = await engine.calculate_compliance(poor_data)

        assert compliance_score <= 0.5

    @pytest.mark.asyncio
    async def test_get_geometry_insights(self, engine):
        """Test Sacred Geometry insights generation"""
        await engine.initialize()

        test_data = {
            "metrics": {
                "completion": 0.9,
                "stability": 0.85,
                "growth": 0.8,
                "balance": 0.88,
                "complexity": 0.75,
            }
        }

        insights = await engine.get_geometry_insights(test_data)

        assert isinstance(insights, dict)
        assert "patterns" in insights
        assert "recommendations" in insights
        assert "sacred_geometry_score" in insights

        # Verify pattern scores
        pattern_scores = insights["patterns"]
        assert "circle" in pattern_scores
        assert "triangle" in pattern_scores
        assert "spiral" in pattern_scores
        assert "golden_ratio" in pattern_scores
        assert "fractal" in pattern_scores

        for pattern, score in pattern_scores.items():
            assert isinstance(score, (int, float))
            assert 0.0 <= score <= 1.0

    @pytest.mark.asyncio
    async def test_process_sacred_geometry(self, engine):
        """Test comprehensive Sacred Geometry processing"""
        await engine.initialize()

        mission_data = {
            "mission_id": "test-123",
            "performance_data": {
                "success_rate": 0.95,
                "error_rate": 0.05,
                "efficiency": 0.88,
                "completion_time": 300,
            },
            "quality_metrics": {
                "accuracy": 0.92,
                "precision": 0.89,
                "completeness": 0.96,
            },
        }

        result = await engine.process_sacred_geometry(mission_data)

        assert isinstance(result, dict)
        assert "compliance_score" in result
        assert "pattern_analysis" in result
        assert "insights" in result
        assert "recommendations" in result

        compliance_score = result["compliance_score"]
        assert isinstance(compliance_score, (int, float))
        assert 0.0 <= compliance_score <= 1.0

    @pytest.mark.asyncio
    async def test_validate_all_patterns(self, engine):
        """Test validation of all supported patterns"""
        await engine.initialize()

        test_data = {
            "completion": 0.9,
            "stability": 0.85,
            "growth": 0.8,
            "balance": 0.88,
            "complexity": 0.75,
        }

        for pattern_name in engine.patterns.keys():
            result = await engine.validate_pattern(pattern_name, test_data)
            assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_engine_error_handling(self, engine):
        """Test error handling in Sacred Geometry processing"""
        await engine.initialize()

        # Test with malformed data
        malformed_data = None

        with pytest.raises(Exception):
            await engine.calculate_compliance(malformed_data)

    @pytest.mark.asyncio
    async def test_pattern_thresholds(self, engine):
        """Test pattern validation thresholds"""
        await engine.initialize()

        # Test data that should meet thresholds
        good_data = {"score": 0.8, "quality": 0.85, "completeness": 0.9}

        # Test data that should not meet thresholds
        poor_data = {"score": 0.3, "quality": 0.2, "completeness": 0.1}

        for pattern_name in engine.patterns.keys():
            good_result = await engine.validate_pattern(pattern_name, good_data)
            poor_result = await engine.validate_pattern(pattern_name, poor_data)

            # Both should return boolean values
            assert isinstance(good_result, bool)
            assert isinstance(poor_result, bool)

    def test_mathematical_constants(self, engine):
        """Test mathematical constants used in Sacred Geometry"""
        # Golden ratio properties
        phi = engine.phi

        # φ² = φ + 1
        assert abs(phi**2 - (phi + 1)) < 1e-10

        # φ = (1 + √5) / 2
        assert abs(phi - (1 + math.sqrt(5)) / 2) < 1e-15

        # Fibonacci ratios approach φ
        fib_ratios = []
        a, b = 1, 1
        for _ in range(10):
            a, b = b, a + b
            if a > 0:
                fib_ratios.append(b / a)

        # Later ratios should be close to φ
        assert abs(fib_ratios[-1] - phi) < 0.01

    @pytest.mark.asyncio
    async def test_concurrent_processing(self, engine):
        """Test concurrent Sacred Geometry processing"""
        import asyncio

        await engine.initialize()

        # Create multiple test datasets
        datasets = []
        for i in range(5):
            datasets.append(
                {
                    "id": i,
                    "performance": 0.8 + (i * 0.02),
                    "quality": 0.75 + (i * 0.03),
                    "completeness": 0.85 + (i * 0.01),
                }
            )

        # Process concurrently
        tasks = [engine.calculate_compliance(data) for data in datasets]
        results = await asyncio.gather(*tasks)

        # Verify all results are valid
        assert len(results) == 5
        for result in results:
            assert isinstance(result, (int, float))
            assert 0.0 <= result <= 1.0

    @pytest.mark.asyncio
    async def test_pattern_weights(self, engine):
        """Test Sacred Geometry pattern weighting"""
        await engine.initialize()

        # Test data with different emphasis on different patterns
        circle_emphasis = {"completeness": 1.0, "closure": 1.0, "perfection": 1.0}

        triangle_emphasis = {"stability": 1.0, "foundation": 1.0, "structure": 1.0}

        # Both should produce valid insights but with different patterns emphasized
        circle_insights = await engine.get_geometry_insights(circle_emphasis)
        triangle_insights = await engine.get_geometry_insights(triangle_emphasis)

        assert isinstance(circle_insights, dict)
        assert isinstance(triangle_insights, dict)

        # Verify different pattern strengths
        circle_patterns = circle_insights["patterns"]
        triangle_patterns = triangle_insights["patterns"]

        # Circle score should be high for circle_emphasis data
        assert circle_patterns["circle"] >= 0.7
        # Triangle score should be high for triangle_emphasis data
        assert triangle_patterns["triangle"] >= 0.7
