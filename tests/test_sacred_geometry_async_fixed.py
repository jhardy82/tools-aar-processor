"""
🧪 Sacred Geometry Engine Unit Tests - Async Fixed Version
Tests that match the actual async SacredGeometryEngine API
"""

import asyncio

from src.sacred_geometry_engine import SacredGeometryEngine


class TestSacredGeometryEngineAsyncFixed:
    """Test suite for SacredGeometryEngine class - handles async methods"""

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

    def test_is_healthy_sync(self):
        """Test is_healthy method (sync method)"""
        engine = SacredGeometryEngine()

        # Test that is_healthy returns a boolean
        health = engine.is_healthy()
        assert isinstance(health, bool)

    def test_generate_aar_id_sync(self):
        """Test generate_aar_id method (sync method)"""
        engine = SacredGeometryEngine()

        # Test AAR ID generation
        aar_id = engine.generate_aar_id()
        assert isinstance(aar_id, str)
        assert len(aar_id) > 0

    async def test_initialize_async(self):
        """Test async initialize method"""
        engine = SacredGeometryEngine()

        # Should not raise exceptions
        await engine.initialize()

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

    async def test_validate_patterns_async(self):
        """Test async validate_patterns method"""
        engine = SacredGeometryEngine()

        # Test with sample data
        test_data = {
            "pattern_test": "some_pattern",
            "values": [1, 2, 3, 5, 8],  # Fibonacci-like
        }

        result = await engine.validate_patterns(test_data)
        assert isinstance(result, dict)

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

    async def test_pattern_validation_with_golden_ratio_values(self):
        """Test pattern validation with golden ratio related values"""
        engine = SacredGeometryEngine()

        golden_ratio_data = {
            "values": [1, PHI, PHI_SQUARED],  # φ related values
            "ratios": [PHI],
        }

        result = await engine.validate_patterns(golden_ratio_data)
        assert isinstance(result, dict)

    async def test_pattern_validation_with_fibonacci_sequence(self):
        """Test pattern validation with Fibonacci sequence"""
        engine = SacredGeometryEngine()

        fibonacci_data = {"sequence": [1, 1, 2, 3, 5, 8, 13, 21], "type": "fibonacci"}

        result = await engine.validate_patterns(fibonacci_data)
        assert isinstance(result, dict)

    async def test_complex_data_structure_validation(self):
        """Test validation with complex nested data structures"""
        engine = SacredGeometryEngine()

        complex_data = {
            "metadata": {
                "version": "1.0",
                "created": "2025-06-18",
                "patterns": ["circle", "triangle", "spiral"],
            },
            "measurements": {
                "ratios": [1.0, PHI, PHI_SQUARED],
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

        pattern_result = await engine.validate_patterns(complex_data)
        assert isinstance(pattern_result, dict)


def run_sync_tests():
    """Run synchronous tests"""
    test = TestSacredGeometryEngineAsyncFixed()

    sync_tests = [
        ("test_initialization", test.test_initialization),
        ("test_is_healthy_sync", test.test_is_healthy_sync),
        ("test_generate_aar_id_sync", test.test_generate_aar_id_sync),
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
    test = TestSacredGeometryEngineAsyncFixed()

    async_tests = [
        ("test_initialize_async", test.test_initialize_async),
        ("test_validate_data_async", test.test_validate_data_async),
        ("test_validate_patterns_async", test.test_validate_patterns_async),
        (
            "test_data_validation_with_simple_data",
            test.test_data_validation_with_simple_data,
        ),
        (
            "test_pattern_validation_with_golden_ratio_values",
            test.test_pattern_validation_with_golden_ratio_values,
        ),
        (
            "test_pattern_validation_with_fibonacci_sequence",
            test.test_pattern_validation_with_fibonacci_sequence,
        ),
        (
            "test_complex_data_structure_validation",
            test.test_complex_data_structure_validation,
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

    print("Testing Sacred Geometry Engine with proper async handling")
    print("=" * 60)

    sync_success = run_sync_tests()
    async_success = asyncio.run(run_async_tests())

    if sync_success and async_success:
        print("\n🎉 All Sacred Geometry Engine tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Sacred Geometry Engine tests failed!")
        sys.exit(1)
