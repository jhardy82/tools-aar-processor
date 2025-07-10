#!/usr/bin/env python3
"""
Test runner for monitoring integration tests
"""

import asyncio
import sys

sys.path.insert(0, ".")

from tests.test_monitoring_simple import TestMonitoringIntegrationSimple


def run_sync_tests():
    test = TestMonitoringIntegrationSimple()

    tests = [
        ("test_initialization", test.test_initialization),
        ("test_is_connected_initial_state", test.test_is_connected_initial_state),
        ("test_get_sacred_geometry_context", test.test_get_sacred_geometry_context),
        ("test_monitoring_urls_configuration", test.test_monitoring_urls_configuration),
        (
            "test_sacred_geometry_context_completeness",
            test.test_sacred_geometry_context_completeness,
        ),
        (
            "test_monitoring_integration_attributes",
            test.test_monitoring_integration_attributes,
        ),
        (
            "test_monitoring_integration_methods",
            test.test_monitoring_integration_methods,
        ),
        ("test_private_methods_exist", test.test_private_methods_exist),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
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
    test = TestMonitoringIntegrationSimple()

    tests = [
        ("test_disconnect_without_connection", test.test_disconnect_without_connection),
        ("test_connect_with_mock_fallback", test.test_connect_with_mock_fallback),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
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
    print("Running Monitoring Integration Tests")
    print("=" * 50)

    print("\nRunning sync tests...")
    sync_success = run_sync_tests()

    print("\nRunning async tests...")
    async_success = asyncio.run(run_async_tests())

    if sync_success and async_success:
        print("\n🎉 All monitoring integration tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
