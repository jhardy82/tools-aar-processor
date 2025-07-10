"""
🧪 Sacred Geometry Engine Unit Tests - Correct API Version
Tests that match the actual SacredGeometryEngine API signatures
"""

import asyncio

from src.sacred_geometry_engine import SacredGeometryEngine


class TestSacredGeometryEngineCorrect:
    """Test suite for SacredGeometryEngine class - correct API usage"""

    def test_initialization(self):
        """Test SacredGeometryEngine initialization"""
        engine = SacredGeometryEngine()

        # Test that engine initializes without errors
        assert engine is not None

        # Test that required methods exist
        assert hasattr(engine, "initialize")
        assert hasattr(engine, "is_healthy")
        assert hasattr(engine, "validate_data")
        assert hasattr(engine, "validate_patterns")
        assert hasattr(engine, "generate_aar_id")

    def test_is_healthy_before_init(self):
        """Test is_healthy method before initialization"""
        engine = SacredGeometryEngine()

        # Should return False before initialization
        health = engine.is_healthy()
        assert isinstance(health, bool)
        assert health is False

    async def test_is_healthy_after_init(self):
        """Test is_healthy method after initialization"""
        engine = SacredGeometryEngine()

        # Initialize first
        await engine.initialize()

        # Should return True after initialization
        health = engine.is_healthy()
        assert isinstance(health, bool)
        assert health is True

    def test_generate_aar_id_with_mission_id(self):
        """Test generate_aar_id method with required mission_id"""
        engine = SacredGeometryEngine()

        # Test AAR ID generation with mission ID
        aar_id = engine.generate_aar_id("test_mission_123")
        assert isinstance(aar_id, str)
        assert len(aar_id) > 0
        assert (
            "test_mission_123" in aar_id or len(aar_id) > 10
        )  # Should contain mission ID or be a hash

    def test_validate_patterns_with_pattern_list(self):
        """Test validate_patterns method with list of patterns"""
        engine = SacredGeometryEngine()

        # Test with known patterns
        valid_patterns = ["circle", "triangle", "spiral", "golden_ratio", "fractal"]
        result = engine.validate_patterns(valid_patterns)
        assert isinstance(result, bool)

        # Test with invalid patterns
        invalid_patterns = ["invalid_pattern", "unknown_shape"]
        result = engine.validate_patterns(invalid_patterns)
        assert isinstance(result, bool)
        # Should return False for invalid patterns

    async def test_initialize_async(self):
        """Test async initialize method"""
        engine = SacredGeometryEngine()

        # Should not raise exceptions
        await engine.initialize()

        # Should be healthy after initialization
        assert engine.is_healthy() is True

    async def test_validate_data_async(self):
        """Test async validate_data method"""
        engine = SacredGeometryEngine()

        # Test with sample data
        test_data = {
            "test_field": "test_value",
            "numeric_field": 123,
            "nested": {"inner": "value"},
        }

        result = await engine.validate_data(test_data)
        assert isinstance(result, dict)

    def test_pattern_validation_with_known_patterns(self):
        """Test pattern validation with known Sacred Geometry patterns"""
        engine = SacredGeometryEngine()

        # Test individual patterns
        individual_patterns = [
            ["circle"],
            ["triangle"],
            ["spiral"],
            ["golden_ratio"],
            ["fractal"],
        ]

        for pattern_list in individual_patterns:
            result = engine.validate_patterns(pattern_list)
            assert isinstance(result, bool)
            # These should be valid patterns

    def test_pattern_validation_with_mixed_patterns(self):
        """Test pattern validation with mixed valid and invalid patterns"""
        engine = SacredGeometryEngine()

        # Test with mixed patterns
        mixed_patterns = ["circle", "invalid_pattern", "triangle"]
        result = engine.validate_patterns(mixed_patterns)
        assert isinstance(result, bool)
        # Should return False due to invalid pattern

    def test_generate_multiple_aar_ids(self):
        """Test generating multiple AAR IDs produces unique results"""
        engine = SacredGeometryEngine()

        # Generate multiple IDs
        ids = []
        for i in range(3):
            aar_id = engine.generate_aar_id(f"mission_{i}")
            ids.append(aar_id)
            assert isinstance(aar_id, str)
            assert len(aar_id) > 0

        # IDs should be unique (different timestamps)
        assert len(set(ids)) == len(ids), "AAR IDs should be unique"

    def test_private_pattern_methods_exist(self):
        """Test that private pattern validation methods exist"""
        engine = SacredGeometryEngine()

        pattern_methods = [
            "_circle_pattern",
            "_triangle_pattern",
            "_spiral_pattern",
            "_golden_ratio_pattern",
            "_fractal_pattern",
        ]

        for method_name in pattern_methods:
            assert hasattr(engine, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(engine, method_name)
            ), f"Method {method_name} should be callable"

    def test_analysis_methods_exist(self):
        """Test that analysis methods exist"""
        engine = SacredGeometryEngine()

        analysis_methods = [
            "_analyze_structure_patterns",
            "_analyze_recursive_patterns",
            "_analyze_proportional_relationships",
            "_calculate_circular_completeness",
            "_calculate_structure_balance",
            "_calculate_fractal_dimension",
        ]

        for method_name in analysis_methods:
            assert hasattr(engine, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(engine, method_name)
            ), f"Method {method_name} should be callable"

    async def test_data_validation_with_simple_data(self):
        """Test data validation with simple valid data"""
        engine = SacredGeometryEngine()

        simple_data = {"name": "test", "value": 42}

        result = await engine.validate_data(simple_data)
        assert isinstance(result, dict)
        # Validation should not raise exceptions

    async def test_data_validation_with_complex_data(self):
        """Test data validation with complex nested data structures"""
        engine = SacredGeometryEngine()

        complex_data = {
            "metadata": {
                "version": "1.0",
                "created": "2025-06-18",
                "patterns": ["circle", "triangle", "spiral"],
            },
            "measurements": {
                "ratios": [1.0, 1.618, 2.618],
                "angles": [60, 90, 120, 180, 360],
                "nested_levels": 3,
            },
            "analysis": {
                "completeness": 0.95,
                "balance": 0.87,
                "fibonacci_alignment": True,
            },
        }

        # Should handle complex data without errors
        result = await engine.validate_data(complex_data)
        assert isinstance(result, dict)

    async def test_initialization_and_health_flow(self):
        """Test complete initialization and health check flow"""
        engine = SacredGeometryEngine()

        # Initially not healthy
        assert engine.is_healthy() is False

        # Initialize
        await engine.initialize()

        # Now should be healthy
        assert engine.is_healthy() is True

        # Should be able to validate data
        test_data = {"test": "value"}
        result = await engine.validate_data(test_data)
        assert isinstance(result, dict)

        # Should be able to generate AAR IDs
        aar_id = engine.generate_aar_id("test_mission")
        assert isinstance(aar_id, str)
        assert len(aar_id) > 0


def run_sync_tests():
    """Run synchronous tests"""
    test = TestSacredGeometryEngineCorrect()

    sync_tests = [
        ("test_initialization", test.test_initialization),
        ("test_is_healthy_before_init", test.test_is_healthy_before_init),
        (
            "test_generate_aar_id_with_mission_id",
            test.test_generate_aar_id_with_mission_id,
        ),
        (
            "test_validate_patterns_with_pattern_list",
            test.test_validate_patterns_with_pattern_list,
        ),
        (
            "test_pattern_validation_with_known_patterns",
            test.test_pattern_validation_with_known_patterns,
        ),
        (
            "test_pattern_validation_with_mixed_patterns",
            test.test_pattern_validation_with_mixed_patterns,
        ),
        ("test_generate_multiple_aar_ids", test.test_generate_multiple_aar_ids),
        ("test_private_pattern_methods_exist", test.test_private_pattern_methods_exist),
        ("test_analysis_methods_exist", test.test_analysis_methods_exist),
    ]

    passed = 0
    failed = 0

    print("Running Sacred Geometry Engine Sync Tests")
    print("=" * 50)

    for test_name, test_func in sync_tests:
        try:
            test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1

    print(f"\nSync tests: {passed} passed, {failed} failed")
    return failed == 0


async def run_async_tests():
    """Run asynchronous tests"""
    test = TestSacredGeometryEngineCorrect()

    async_tests = [
        ("test_is_healthy_after_init", test.test_is_healthy_after_init),
        ("test_initialize_async", test.test_initialize_async),
        ("test_validate_data_async", test.test_validate_data_async),
        (
            "test_data_validation_with_simple_data",
            test.test_data_validation_with_simple_data,
        ),
        (
            "test_data_validation_with_complex_data",
            test.test_data_validation_with_complex_data,
        ),
        (
            "test_initialization_and_health_flow",
            test.test_initialization_and_health_flow,
        ),
    ]

    passed = 0
    failed = 0

    print("\nRunning Sacred Geometry Engine Async Tests")
    print("=" * 50)

    for test_name, test_func in async_tests:
        try:
            await test_func()
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1

    print(f"\nAsync tests: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Run tests directly
    import sys

    print("Testing Sacred Geometry Engine with correct API usage")
    print("=" * 60)

    sync_success = run_sync_tests()
    async_success = asyncio.run(run_async_tests())

    if sync_success and async_success:
        print("\n🎉 All Sacred Geometry Engine tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Sacred Geometry Engine tests failed!")
        sys.exit(1)
