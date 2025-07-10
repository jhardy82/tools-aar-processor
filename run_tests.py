#!/usr/bin/env python3
"""
🧪 Test Runner for Sacred Geometry AAR Processor
Comprehensive test execution with detailed reporting
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(command, description=""):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Run Sacred Geometry AAR Processor tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--parallel", "-n", type=int, default=1, help="Number of parallel processes")
    parser.add_argument("--markers", "-m", help="Run tests with specific markers")
    parser.add_argument("--file", "-f", help="Run specific test file")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only (exclude slow tests)")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML coverage report")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmarks")

    args = parser.parse_args()

    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    print("🌀 Sacred Geometry AAR Processor Test Suite")
    print(f"📅 Started at: {datetime.now()}")
    print(f"📂 Working directory: {os.getcwd()}")

    # Base pytest command
    pytest_cmd = ["python", "-m", "pytest"]

    # Add verbosity
    if args.verbose:
        pytest_cmd.append("-v")

    # Add parallel processing
    if args.parallel > 1:
        pytest_cmd.extend(["-n", str(args.parallel)])

    # Add markers
    if args.markers:
        pytest_cmd.extend(["-m", args.markers])
    elif args.unit:
        pytest_cmd.extend(["-m", "unit"])
    elif args.integration:
        pytest_cmd.extend(["-m", "integration"])
    elif args.quick:
        pytest_cmd.extend(["-m", "not slow"])

    # Add specific file
    if args.file:
        pytest_cmd.append(args.file)

    # Add coverage options
    if args.coverage or args.html_report:
        pytest_cmd.extend(["--cov=src", "--cov-report=term-missing"])

        if args.html_report:
            pytest_cmd.extend(["--cov-report=html"])

    # Add benchmark options
    if args.benchmark:
        pytest_cmd.extend(["--benchmark-only"])

    # Run the tests
    print("\n🚀 Running tests...")
    success = run_command(pytest_cmd, "Running pytest")

    if success:
        print("\n✅ All tests completed successfully!")

        # Generate additional reports if requested
        if args.html_report:
            print("\n📊 HTML coverage report generated in 'htmlcov' directory")

        # Run additional quality checks
        print("\n🔍 Running code quality checks...")

        # Type checking
        mypy_success = run_command(
            ["python", "-m", "mypy", "src", "--ignore-missing-imports"],
            "Type checking with mypy",
        )

        # Code formatting check
        black_success = run_command(
            ["python", "-m", "black", "--check", "src", "tests"],
            "Code formatting check with black",
        )

        # Import sorting check
        isort_success = run_command(
            ["python", "-m", "isort", "--check-only", "src", "tests"],
            "Import sorting check with isort",
        )

        # Final summary
        print(f"\n{'='*60}")
        print("📋 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Tests: {'PASSED' if success else 'FAILED'}")
        print(f"✅ Type checking: {'PASSED' if mypy_success else 'FAILED'}")
        print(f"✅ Code formatting: {'PASSED' if black_success else 'FAILED'}")
        print(f"✅ Import sorting: {'PASSED' if isort_success else 'FAILED'}")

        overall_success = all([success, mypy_success, black_success, isort_success])
        print(f"\n🎯 Overall: {'ALL CHECKS PASSED' if overall_success else 'SOME CHECKS FAILED'}")

        return 0 if overall_success else 1

    else:
        print("\n❌ Tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
