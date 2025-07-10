#!/usr/bin/env python3
"""
🧪 Sacred Geometry AAR Processor - Complete Test Suite Runner
Runs all fixed unit tests and provides comprehensive results
"""

import asyncio
import sys
import time
from typing import Dict, Tuple

# Add current directory to path for imports
sys.path.insert(0, ".")

from tests.test_compliance_checker_async_correct import (
    TestComplianceCheckerAsyncCorrect,
)

# Import all test modules
from tests.test_database_manager_fixed import TestDatabaseManager
from tests.test_monitoring_simple import TestMonitoringIntegrationSimple
from tests.test_sacred_geometry_correct import TestSacredGeometryEngineCorrect


class TestResults:
    """Track test results across all modules"""

    def __init__(self):
        self.modules: Dict[str, Dict[str, int]] = {}
        self.total_passed = 0
        self.total_failed = 0
        self.start_time = time.time()

    def add_module_results(self, module_name: str, passed: int, failed: int):
        """Add results for a module"""
        self.modules[module_name] = {"passed": passed, "failed": failed}
        self.total_passed += passed
        self.total_failed += failed

    def print_summary(self):
        """Print comprehensive test summary"""
        elapsed = time.time() - self.start_time

        print("\n" + "=" * 80)
        print("🧪 SACRED GEOMETRY AAR PROCESSOR - TEST SUMMARY")
        print("=" * 80)

        for module_name, results in self.modules.items():
            passed = results["passed"]
            failed = results["failed"]
            total = passed + failed
            success_rate = (passed / total * 100) if total > 0 else 0

            status = "✅ PASS" if failed == 0 else "❌ FAIL"
            print(f"{status} {module_name:<35} {passed:>3}/{total:<3} ({success_rate:>5.1f}%)")

        print("-" * 80)
        total_tests = self.total_passed + self.total_failed
        overall_success_rate = (self.total_passed / total_tests * 100) if total_tests > 0 else 0

        print(f"{'TOTAL':<40} {self.total_passed:>3}/{total_tests:<3} ({overall_success_rate:>5.1f}%)")
        print(f"Execution time: {elapsed:.2f} seconds")

        if self.total_failed == 0:
            print("\n🎉 ALL TESTS PASSED! The Sacred Geometry AAR Processor is ready.")
        else:
            print(f"\n❌ {self.total_failed} tests failed. Review and fix before deployment.")

        return self.total_failed == 0


def run_database_tests() -> Tuple[int, int]:
    """Run database manager tests"""
    print("🗃️  Testing Database Manager...")
    test = TestDatabaseManager()

    tests = [
        ("test_initialization", test.test_initialization),
        ("test_initialize_database", test.test_initialize_database),
        ("test_is_healthy", test.test_is_healthy),
        ("test_store_and_retrieve_aar", test.test_store_and_retrieve_aar),
        ("test_get_aar_status", test.test_get_aar_status),
        ("test_get_aar_report", test.test_get_aar_report),
        ("test_list_aars", test.test_list_aars),
        ("test_get_compliance_stats", test.test_get_compliance_stats),
        ("test_context_manager", test.test_context_manager),
        ("test_database_error_handling", test.test_database_error_handling),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            asyncio.run(test_func())
            print(f"  ✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test_name}: {e}")
            failed += 1

    return passed, failed


def run_monitoring_tests() -> Tuple[int, int]:
    """Run monitoring integration tests"""
    print("📊 Testing Monitoring Integration...")
    test = TestMonitoringIntegrationSimple()

    # Sync tests
    sync_tests = [
        ("test_initialization", test.test_initialization),
        ("test_is_connected_initial_state", test.test_is_connected_initial_state),
        ("test_get_sacred_geometry_context", test.test_get_sacred_geometry_context),
        ("test_monitoring_urls_configuration", test.test_monitoring_urls_configuration),
        ("test_sacred_geometry_context_completeness", test.test_sacred_geometry_context_completeness),
        ("test_monitoring_integration_attributes", test.test_monitoring_integration_attributes),
        ("test_monitoring_integration_methods", test.test_monitoring_integration_methods),
        ("test_private_methods_exist", test.test_private_methods_exist),
    ]

    # Async tests
    async_tests = [
        ("test_disconnect_without_connection", test.test_disconnect_without_connection),
        ("test_connect_with_mock_fallback", test.test_connect_with_mock_fallback),
    ]

    passed = 0
    failed = 0

    # Run sync tests
    for test_name, test_func in sync_tests:
        try:
            test_func()
            print(f"  ✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test_name}: {e}")
            failed += 1

    # Run async tests
    async def run_async_monitoring_tests():
        nonlocal passed, failed
        for test_name, test_func in async_tests:
            try:
                await test_func()
                print(f"  ✓ {test_name}")
                passed += 1
            except Exception as e:
                print(f"  ✗ {test_name}: {e}")
                failed += 1

    asyncio.run(run_async_monitoring_tests())

    return passed, failed


def run_sacred_geometry_tests() -> Tuple[int, int]:
    """Run Sacred Geometry Engine tests"""
    print("🔮 Testing Sacred Geometry Engine...")
    test = TestSacredGeometryEngineCorrect()

    # Sync tests
    sync_tests = [
        ("test_initialization", test.test_initialization),
        ("test_is_healthy_before_init", test.test_is_healthy_before_init),
        ("test_generate_aar_id_with_mission_id", test.test_generate_aar_id_with_mission_id),
        ("test_validate_patterns_with_pattern_list", test.test_validate_patterns_with_pattern_list),
        ("test_pattern_validation_with_known_patterns", test.test_pattern_validation_with_known_patterns),
        ("test_pattern_validation_with_mixed_patterns", test.test_pattern_validation_with_mixed_patterns),
        ("test_generate_multiple_aar_ids", test.test_generate_multiple_aar_ids),
        ("test_private_pattern_methods_exist", test.test_private_pattern_methods_exist),
        ("test_analysis_methods_exist", test.test_analysis_methods_exist),
    ]

    # Async tests
    async_tests = [
        ("test_is_healthy_after_init", test.test_is_healthy_after_init),
        ("test_initialize_async", test.test_initialize_async),
        ("test_validate_data_async", test.test_validate_data_async),
        ("test_data_validation_with_simple_data", test.test_data_validation_with_simple_data),
        ("test_data_validation_with_complex_data", test.test_data_validation_with_complex_data),
        ("test_initialization_and_health_flow", test.test_initialization_and_health_flow),
    ]

    passed = 0
    failed = 0

    # Run sync tests
    for test_name, test_func in sync_tests:
        try:
            test_func()
            print(f"  ✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test_name}: {e}")
            failed += 1

    # Run async tests
    async def run_async_sg_tests():
        nonlocal passed, failed
        for test_name, test_func in async_tests:
            try:
                await test_func()
                print(f"  ✓ {test_name}")
                passed += 1
            except Exception as e:
                print(f"  ✗ {test_name}: {e}")
                failed += 1

    asyncio.run(run_async_sg_tests())

    return passed, failed


def run_compliance_tests() -> Tuple[int, int]:
    """Run Compliance Checker tests"""
    print("📋 Testing Compliance Checker...")
    test = TestComplianceCheckerAsyncCorrect()

    # Sync tests
    sync_tests = [
        ("test_initialization_requires_sacred_geometry_engine", test.test_initialization_requires_sacred_geometry_engine),
        ("test_required_methods_exist", test.test_required_methods_exist),
        ("test_private_methods_exist", test.test_private_methods_exist),
        ("test_compliance_integration_with_sacred_geometry", test.test_compliance_integration_with_sacred_geometry),
    ]

    # Async tests
    async_tests = [
        ("test_get_current_compliance_async", test.test_get_current_compliance_async),
        ("test_get_detailed_compliance_async", test.test_get_detailed_compliance_async),
        ("test_update_compliance_with_score", test.test_update_compliance_with_score),
        ("test_validate_mission_compliance_with_mission_data", test.test_validate_mission_compliance_with_mission_data),
        ("test_generate_compliance_report_async", test.test_generate_compliance_report_async),
        ("test_check_compliance_alerts_async", test.test_check_compliance_alerts_async),
        ("test_compliance_with_initialized_engine", test.test_compliance_with_initialized_engine),
        ("test_compliance_validation_with_complex_mission", test.test_compliance_validation_with_complex_mission),
        ("test_compliance_update_with_various_scores", test.test_compliance_update_with_various_scores),
        ("test_compliance_alerts_structure", test.test_compliance_alerts_structure),
        ("test_compliance_report_structure", test.test_compliance_report_structure),
        ("test_compliance_score_boundary_values", test.test_compliance_score_boundary_values),
        ("test_compliance_workflow_end_to_end", test.test_compliance_workflow_end_to_end),
    ]

    passed = 0
    failed = 0

    # Run sync tests
    for test_name, test_func in sync_tests:
        try:
            test_func()
            print(f"  ✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {test_name}: {e}")
            failed += 1

    # Run async tests
    async def run_async_compliance_tests():
        nonlocal passed, failed
        for test_name, test_func in async_tests:
            try:
                await test_func()
                print(f"  ✓ {test_name}")
                passed += 1
            except Exception as e:
                print(f"  ✗ {test_name}: {e}")
                failed += 1

    asyncio.run(run_async_compliance_tests())

    return passed, failed


def main():
    """Run all tests and provide comprehensive results"""
    print("🧪 Sacred Geometry AAR Processor - Complete Test Suite")
    print("=" * 60)
    print("Running comprehensive unit tests for all modules...")
    print()

    results = TestResults()

    # Run all test modules
    try:
        # Database Manager Tests
        db_passed, db_failed = run_database_tests()
        results.add_module_results("Database Manager", db_passed, db_failed)
        print()

        # Monitoring Integration Tests
        mon_passed, mon_failed = run_monitoring_tests()
        results.add_module_results("Monitoring Integration", mon_passed, mon_failed)
        print()

        # Sacred Geometry Engine Tests
        sg_passed, sg_failed = run_sacred_geometry_tests()
        results.add_module_results("Sacred Geometry Engine", sg_passed, sg_failed)
        print()

        # Compliance Checker Tests
        comp_passed, comp_failed = run_compliance_tests()
        results.add_module_results("Compliance Checker", comp_passed, comp_failed)
        print()

    except Exception as e:
        print(f"❌ Critical error running tests: {e}")
        return 1

    # Print comprehensive summary
    success = results.print_summary()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
