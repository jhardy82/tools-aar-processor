#!/usr/bin/env python3
"""
Manual test execution - just run one test manually to see what happens
"""

import asyncio
import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, "src")


async def manual_test():
    print("🧪 MANUAL TEST EXECUTION")
    print("=" * 40)

    try:
        print("1. Importing database manager...")
        from src.database_manager import DatabaseManager

        print("✅ Import successful")

        print("2. Creating temporary database...")
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name
        print(f"✅ Temp database: {temp_path}")

        print("3. Creating database manager...")
        db_manager = DatabaseManager(db_path=temp_path)
        print("✅ Database manager created")

        print("4. Testing database initialization...")
        await db_manager.initialize()
        print("✅ Database initialized")

        print("5. Testing health check...")
        health = await db_manager.is_healthy()
        print(f"✅ Health check: {health}")

        print("6. Testing AAR storage...")
        test_aar = {
            "aar_id": "test-123",
            "mission_id": "mission-456",
            "compliance_score": 0.85,
            "report_content": {"status": "test"},
            "metadata": {"version": "1.0"},
        }

        await db_manager.store_aar(test_aar)
        print("✅ AAR stored successfully")

        print("7. Testing AAR retrieval...")
        retrieved = await db_manager.get_aar("test-123")
        print(f"✅ AAR retrieved: {retrieved is not None}")

        print("8. Closing database...")
        await db_manager.close()
        print("✅ Database closed")

        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        print("✅ Cleanup complete")

        print("\n🎉 MANUAL TEST PASSED!")
        return True

    except Exception as e:
        print(f"❌ MANUAL TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(manual_test())
    sys.exit(0 if result else 1)
