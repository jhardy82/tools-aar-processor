#!/usr/bin/env python3
"""
Actual test runner - let's see what really happens
"""

import os
import subprocess
import sys

print("🧪 ACTUAL TEST EXECUTION")
print("=" * 50)

# Change to correct directory
os.chdir(r"c:\Users\James\Documents\Github\GHrepos\Core-Framework\tools\aar\containers\aar-processor")
print(f"Working directory: {os.getcwd()}")

# Test 1: Can we collect tests?
print("\n1. Testing collection...")
try:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_database_manager.py",
            "--collect-only",
            "-q",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )

    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")

except subprocess.TimeoutExpired:
    print("❌ Test collection timed out")
except Exception as e:
    print(f"❌ Error during collection: {e}")

# Test 2: Can we run a single test?
print("\n2. Testing single test execution...")
try:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_database_manager.py::TestDatabaseManager::test_initialization_creates_database",
            "-v",
            "-s",
            "--tb=short",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )

    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")

except subprocess.TimeoutExpired:
    print("❌ Test execution timed out")
except Exception as e:
    print(f"❌ Error during execution: {e}")

# Test 3: Try to import the test module directly
print("\n3. Testing direct import...")
try:
    import tests.test_database_manager

    print("✅ Test module imported successfully")

    # Try to access the test class
    test_class = tests.test_database_manager.TestDatabaseManager
    print("✅ Test class accessible")

except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback

    traceback.print_exc()

print("\n🎯 Test execution complete!")
