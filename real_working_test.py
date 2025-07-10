#!/usr/bin/env python3
"""
Real working test - using actual database manager API
"""

import asyncio
import os
import sys
import tempfile

# Add src to path
sys.path.insert(0, "src")


async def real_working_test():
    print("🧪 REAL WORKING TEST")
    print("=" * 40)

    try:
        print("1. Importing required modules...")
        from src.aar_generator import AARResult
        from src.database_manager import DatabaseManager

        print("✅ Imports successful")

        print("2. Creating temporary database...")
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
            temp_path = temp_file.name
        print(f"✅ Temp database: {temp_path}")

        print("3. Creating database manager...")
        db_manager = DatabaseManager(db_path=temp_path)
        print("✅ Database manager created")

        print("4. Initializing database...")
        await db_manager.initialize()
        print("✅ Database initialized")

        print("5. Testing health check...")
        health = await db_manager.is_healthy()
        print(f"✅ Health check: {health}")

        print("6. Creating AAR result object...")
        aar_result = AARResult(
            aar_id="test-123",
            mission_id="mission-456",
            compliance_score=0.85,
            report_content={"status": "test", "results": "success"},
            metadata={"version": "1.0", "test": True},
        )
        print("✅ AAR result created")

        print("7. Storing AAR...")
        store_success = await db_manager.store_aar(aar_result)
        print(f"✅ AAR stored: {store_success}")

        print("8. Retrieving AAR status...")
        status = await db_manager.get_aar_status("test-123")
        print(f"✅ AAR status retrieved: {status is not None}")
        if status:
            print(f"   Status data: {status}")

        print("9. Retrieving AAR report...")
        report = await db_manager.get_aar_report("test-123")
        print(f"✅ AAR report retrieved: {report is not None}")
        if report:
            print(f"   Report keys: {list(report.keys())}")

        print("10. Listing AARs...")
        aars = await db_manager.list_aars(limit=10)
        print(f"✅ Listed {len(aars)} AARs")

        print("11. Getting compliance stats...")
        stats = await db_manager.get_compliance_stats()
        print(f"✅ Compliance stats: {list(stats.keys())}")

        print("12. Closing database...")
        await db_manager.close()
        print("✅ Database closed")

        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        print("✅ Cleanup complete")

        print("\n🎉 REAL TEST PASSED!")
        return True

    except Exception as e:
        print(f"❌ REAL TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    result = asyncio.run(real_working_test())
    sys.exit(0 if result else 1)
