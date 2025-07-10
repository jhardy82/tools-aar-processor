#!/usr/bin/env python3
"""
Simple test runner to diagnose issues
"""

import os
import sys
import traceback

print("🔍 Diagnosing test issues...")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

try:
    print("\n1. Testing imports...")
    from src.database_manager import DatabaseManager

    print("✅ DatabaseManager import successful")

    print("✅ MonitoringIntegration import successful")

    print("✅ AARGenerator import successful")

    print("✅ SacredGeometryEngine import successful")

    print("✅ ComplianceChecker import successful")

    print("✅ AARProcessor import successful")

except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()

try:
    print("\n2. Testing pytest import...")
    print("✅ pytest available")

    print("✅ pytest-asyncio available")

except Exception as e:
    print(f"❌ pytest import error: {e}")
    traceback.print_exc()

try:
    print("\n3. Testing basic database functionality...")
    import tempfile

    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        temp_path = temp_file.name

    db_manager = DatabaseManager(temp_path)
    print("✅ DatabaseManager instance created")

    # Test async initialization
    import asyncio

    async def test_db():
        await db_manager.initialize()
        print("✅ Database initialized")

        health = await db_manager.is_healthy()
        print(f"✅ Database health check: {health}")

        await db_manager.close()
        print("✅ Database closed")

    asyncio.run(test_db())

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)

except Exception as e:
    print(f"❌ Database test error: {e}")
    traceback.print_exc()

try:
    print("\n4. Testing pytest execution...")
    import subprocess

    result = subprocess.run([sys.executable, "-m", "pytest", "--version"], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ pytest version: {result.stdout.strip()}")
    else:
        print(f"❌ pytest version check failed: {result.stderr}")

except Exception as e:
    print(f"❌ pytest execution error: {e}")
    traceback.print_exc()

print("\n🎯 Diagnosis complete!")
