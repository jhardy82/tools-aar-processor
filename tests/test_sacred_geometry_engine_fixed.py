"""
🧪 Sacred Geometry Engine Unit Tests - Fixed Version
Tests that match the actual SacredGeometryEngine API
"""

from src.sacred_geometry_engine import SacredGeometryEngine


class TestSacredGeometryEngineFixed:
    """Test suite for SacredGeometryEngine class - matches real API"""

    def test_initialization(self):
        """Test SacredGeometryEngine initialization"""
        engine = SacredGeometryEngine()

        # Test that engine initializes without errors
        assert engine is not None

        # Test initialization method exists and can be called
        assert hasattr(engine, "initialize")
        engine.initialize()

    def test_is_healthy(self):
        """Test is_healthy method"""
        engine = SacredGeometryEngine()

        # Test that is_healthy returns a boolean
        health = engine.is_healthy()
        assert isinstance(health, bool)

    def test_validate_data(self):
        """Test validate_data method"""
        engine = SacredGeometryEngine()

        # Test with sample data
        test_data = {
            "test_field": "test_value",
            "numeric_field": 123,
            "nested": {"inner": "value"},
        }

        result = engine.validate_data(test_data)
        assert isinstance(result, dict)

    def test_validate_patterns(self):
        """Test validate_patterns method"""
        engine = SacredGeometryEngine()

        # Test with sample data
        test_data = {
            "pattern_test": "some_pattern",
            "values": [1, 2, 3, 5, 8],  # Fibonacci-like
        }

        result = engine.validate_patterns(test_data)
        assert isinstance(result, dict)

    def test_generate_aar_id(self):
        """Test generate_aar_id method"""
        engine = SacredGeometryEngine()

        # Test AAR ID generation
        aar_id = engine.generate_aar_id()
        assert isinstance(aar_id, str)
        assert len(aar_id) > 0

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

    def test_validation_methods_exist(self):
        """Test that validation helper methods exist"""
        engine = SacredGeometryEngine()

        validation_methods = [
            "_validate_structural_integrity",
            "_validate_content_quality",
            "_validate_contextual_relevance",
            "_check_fibonacci_alignment",
            "_check_error_handling_patterns",
        ]

        for method_name in validation_methods:
            assert hasattr(engine, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(engine, method_name)
            ), f"Method {method_name} should be callable"

    def test_utility_methods_exist(self):
        """Test that utility methods exist"""
        engine = SacredGeometryEngine()

        utility_methods = [
            "_extract_numbers_from_data",
            "_find_golden_ratios_in_values",
            "_detect_self_similarity",
            "_detect_spiral_growth",
            "_count_nesting_levels",
            "_count_elements_by_scale",
            "_calculate_max_depth",
        ]

        for method_name in utility_methods:
            assert hasattr(engine, method_name), f"Missing method: {method_name}"
            assert callable(
                getattr(engine, method_name)
            ), f"Method {method_name} should be callable"

    def test_data_validation_with_simple_data(self):
        """Test data validation with simple valid data"""
        engine = SacredGeometryEngine()

        simple_data = {"name": "test", "value": 42}

        result = engine.validate_data(simple_data)
        assert isinstance(result, dict)
        # Validation should not raise exceptions

    def test_pattern_validation_with_golden_ratio_values(self):
        """Test pattern validation with golden ratio related values"""
        engine = SacredGeometryEngine()

        golden_ratio_data = {
            "values": [1, PHI, PHI_SQUARED],  # φ related values
            "ratios": [PHI],
        }

        result = engine.validate_patterns(golden_ratio_data)
        assert isinstance(result, dict)

    def test_pattern_validation_with_fibonacci_sequence(self):
        """Test pattern validation with Fibonacci sequence"""
        engine = SacredGeometryEngine()

        fibonacci_data = {"sequence": [1, 1, 2, 3, 5, 8, 13, 21], "type": "fibonacci"}

        result = engine.validate_patterns(fibonacci_data)
        assert isinstance(result, dict)

    def test_engine_methods_return_appropriate_types(self):
        """Test that engine methods return expected types"""
        engine = SacredGeometryEngine()

        # Test basic methods
        assert isinstance(engine.is_healthy(), bool)
        assert isinstance(engine.generate_aar_id(), str)

        # Test validation methods with minimal data
        test_data = {"test": "data"}
        assert isinstance(engine.validate_data(test_data), dict)
        assert isinstance(engine.validate_patterns(test_data), dict)

    def test_engine_initialize_patterns(self):
        """Test that _initialize_patterns method exists and works"""
        engine = SacredGeometryEngine()

        assert hasattr(engine, "_initialize_patterns")
        # Should not raise exceptions
        engine._initialize_patterns()

    def test_complex_data_structure_validation(self):
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
        result = engine.validate_data(complex_data)
        assert isinstance(result, dict)

        pattern_result = engine.validate_patterns(complex_data)
        assert isinstance(pattern_result, dict)


if __name__ == "__main__":
    # Allow running tests directly
    def run_tests():
        test = TestSacredGeometryEngineFixed()

        tests = [
            ("test_initialization", test.test_initialization),
            ("test_is_healthy", test.test_is_healthy),
            ("test_validate_data", test.test_validate_data),
            ("test_validate_patterns", test.test_validate_patterns),
            ("test_generate_aar_id", test.test_generate_aar_id),
            (
                "test_private_pattern_methods_exist",
                test.test_private_pattern_methods_exist,
            ),
            ("test_analysis_methods_exist", test.test_analysis_methods_exist),
            ("test_validation_methods_exist", test.test_validation_methods_exist),
            ("test_utility_methods_exist", test.test_utility_methods_exist),
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
                "test_engine_methods_return_appropriate_types",
                test.test_engine_methods_return_appropriate_types,
            ),
            ("test_engine_initialize_patterns", test.test_engine_initialize_patterns),
            (
                "test_complex_data_structure_validation",
                test.test_complex_data_structure_validation,
            ),
        ]

        passed = 0
        failed = 0

        print("Running Sacred Geometry Engine Tests")
        print("=" * 50)

        for test_name, test_func in tests:
            try:
                test_func()
                print(f"✓ {test_name}")
                passed += 1
            except Exception as e:
                print(f"✗ {test_name}: {e}")
                failed += 1

        print(f"\nSacred Geometry Engine tests: {passed} passed, {failed} failed")

        if failed == 0:
            print("🎉 All Sacred Geometry Engine tests passed!")
            return True
        else:
            print("❌ Some Sacred Geometry Engine tests failed!")
            return False

    run_tests()
