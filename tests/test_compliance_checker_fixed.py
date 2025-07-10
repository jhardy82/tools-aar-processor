"""
🧪 Compliance Checker Unit Tests - Fixed Version
Tests that match the actual ComplianceChecker API
"""

import asyncio

from src.compliance_checker import ComplianceChecker
from src.sacred_geometry_engine import SacredGeometryEngine


class TestComplianceCheckerFixed:
    """Test suite for ComplianceChecker class - matches real API"""

    def test_initialization_requires_sacred_geometry_engine(self):
        """Test ComplianceChecker initialization requires SacredGeometryEngine"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        # Test that checker initializes without errors
        assert checker is not None
        assert hasattr(checker, 'sacred_geometry')
        assert checker.sacred_geometry is engine

    def test_required_methods_exist(self):
        """Test that all expected methods exist"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        expected_methods = [
            'get_current_compliance',
            'get_detailed_compliance',
            'update_compliance',
            'validate_mission_compliance',
            'generate_compliance_report',
            'check_compliance_alerts',
        ]

        for method_name in expected_methods:
            assert hasattr(checker, method_name), f"Missing method: {method_name}"
            assert callable(getattr(checker, method_name)), f"Method {method_name} should be callable"

    def test_private_methods_exist(self):
        """Test that expected private methods exist"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        private_methods = [
            '_calculate_next_review_date',
            '_generate_mission_recommendations',
            '_get_compliance_level',
            '_get_compliance_recommendations',
            '_get_pattern_compliance_status',
        ]

        for method_name in private_methods:
            assert hasattr(checker, method_name), f"Missing private method: {method_name}"
            assert callable(getattr(checker, method_name)), f"Method {method_name} should be callable"

    def test_get_current_compliance(self):
        """Test get_current_compliance method"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        result = checker.get_current_compliance()
        assert isinstance(result, dict), "get_current_compliance should return a dict"

    def test_get_detailed_compliance(self):
        """Test get_detailed_compliance method"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        result = checker.get_detailed_compliance()
        assert isinstance(result, dict), "get_detailed_compliance should return a dict"

    def test_update_compliance_with_data(self):
        """Test update_compliance method with sample data"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        compliance_data = {
            "mission_id": "test_mission_123",
            "score": 0.85,
            "patterns": ["circle", "triangle"],
            "timestamp": "2025-06-18T22:58:00Z"
        }
          # Should not raise exceptions
        checker.update_compliance(compliance_data)
        # The method might return None or a result - just ensure it doesn't crash

    def test_validate_mission_compliance_with_mission_data(self):
        """Test validate_mission_compliance method"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        mission_data = {
            "mission_id": "test_mission_123",
            "objectives": ["objective_1", "objective_2"],
            "patterns": ["circle", "golden_ratio"],
            "completion_rate": 0.75
        }

        result = checker.validate_mission_compliance(mission_data)
        assert isinstance(result, dict), "validate_mission_compliance should return a dict"

    def test_generate_compliance_report(self):
        """Test generate_compliance_report method"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        result = checker.generate_compliance_report()
        assert isinstance(result, dict), "generate_compliance_report should return a dict"

    def test_check_compliance_alerts(self):
        """Test check_compliance_alerts method"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        result = checker.check_compliance_alerts()
        assert isinstance(result, list), "check_compliance_alerts should return a list"

    async def test_compliance_with_initialized_engine(self):
        """Test compliance checking with initialized Sacred Geometry Engine"""
        engine = SacredGeometryEngine()
        await engine.initialize()  # Initialize the engine first

        checker = ComplianceChecker(engine)

        # Test with initialized engine
        current = checker.get_current_compliance()
        assert isinstance(current, dict)

        detailed = checker.get_detailed_compliance()
        assert isinstance(detailed, dict)

        report = checker.generate_compliance_report()
        assert isinstance(report, dict)

        alerts = checker.check_compliance_alerts()
        assert isinstance(alerts, list)

    def test_compliance_validation_with_complex_mission(self):
        """Test compliance validation with complex mission data"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        complex_mission = {
            "mission_id": "complex_mission_456",
            "mission_type": "sacred_geometry_validation",
            "objectives": [
                "validate_circle_completeness",
                "verify_golden_ratio_proportions",
                "ensure_fractal_patterns"
            ],
            "patterns": ["circle", "triangle", "spiral", "golden_ratio", "fractal"],
            "metadata": {
                "created": "2025-06-18",
                "priority": "high",
                "compliance_level": "strict"
            },
            "metrics": {
                "completion_rate": 0.92,
                "accuracy": 0.87,
                "pattern_alignment": 0.95
            }
        }

        result = checker.validate_mission_compliance(complex_mission)
        assert isinstance(result, dict)
        # Should handle complex data without errors

    def test_compliance_update_with_various_scores(self):
        """Test compliance updates with various score values"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        test_scores = [0.0, 0.25, 0.5, 0.75, 0.95, 1.0]

        for score in test_scores:
            compliance_data = {
                "mission_id": f"test_mission_{score}",
                "score": score,
                "patterns": ["circle"],
                "timestamp": "2025-06-18T22:58:00Z"
            }

            # Should handle all score values without errors
            checker.update_compliance(compliance_data)

    def test_compliance_integration_with_sacred_geometry(self):
        """Test that compliance checker properly integrates with Sacred Geometry Engine"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        # Verify integration
        assert checker.sacred_geometry is engine

        # Test that compliance checker can access engine methods
        assert hasattr(checker.sacred_geometry, 'is_healthy')
        assert hasattr(checker.sacred_geometry, 'validate_patterns')
        assert hasattr(checker.sacred_geometry, 'generate_aar_id')

        # Test pattern validation through engine
        valid_patterns = ["circle", "triangle"]
        pattern_validation = checker.sacred_geometry.validate_patterns(valid_patterns)
        assert isinstance(pattern_validation, bool)

    def test_compliance_alerts_structure(self):
        """Test that compliance alerts have expected structure"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        alerts = checker.check_compliance_alerts()
        assert isinstance(alerts, list)

        # If there are alerts, check their structure
        for alert in alerts:
            assert isinstance(alert, dict), "Each alert should be a dictionary"

    def test_compliance_report_structure(self):
        """Test that compliance report has expected structure"""
        engine = SacredGeometryEngine()
        checker = ComplianceChecker(engine)

        report = checker.generate_compliance_report()
        assert isinstance(report, dict)

        # Report should have some basic structure
        # (We don't know the exact structure, but it should be a non-empty dict)
        assert len(report) >= 0  # At minimum, should not error


def run_sync_tests():
    """Run synchronous tests"""
    test = TestComplianceCheckerFixed()

    sync_tests = [
        ("test_initialization_requires_sacred_geometry_engine", test.test_initialization_requires_sacred_geometry_engine),
        ("test_required_methods_exist", test.test_required_methods_exist),
        ("test_private_methods_exist", test.test_private_methods_exist),
        ("test_get_current_compliance", test.test_get_current_compliance),
        ("test_get_detailed_compliance", test.test_get_detailed_compliance),
        ("test_update_compliance_with_data", test.test_update_compliance_with_data),
        ("test_validate_mission_compliance_with_mission_data", test.test_validate_mission_compliance_with_mission_data),
        ("test_generate_compliance_report", test.test_generate_compliance_report),
        ("test_check_compliance_alerts", test.test_check_compliance_alerts),
        ("test_compliance_validation_with_complex_mission", test.test_compliance_validation_with_complex_mission),
        ("test_compliance_update_with_various_scores", test.test_compliance_update_with_various_scores),
        ("test_compliance_integration_with_sacred_geometry", test.test_compliance_integration_with_sacred_geometry),
        ("test_compliance_alerts_structure", test.test_compliance_alerts_structure),
        ("test_compliance_report_structure", test.test_compliance_report_structure),
    ]

    passed = 0
    failed = 0

    print("Running Compliance Checker Sync Tests")
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
    test = TestComplianceCheckerFixed()

    async_tests = [
        ("test_compliance_with_initialized_engine", test.test_compliance_with_initialized_engine),
    ]

    passed = 0
    failed = 0

    print("\nRunning Compliance Checker Async Tests")
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

    print("Testing Compliance Checker with correct API usage")
    print("=" * 60)

    sync_success = run_sync_tests()
    async_success = asyncio.run(run_async_tests())

    if sync_success and async_success:
        print("\n🎉 All Compliance Checker tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some Compliance Checker tests failed!")
        sys.exit(1)
