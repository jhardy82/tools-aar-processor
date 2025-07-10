# Sacred Geometry AAR Processor Tests

This directory contains comprehensive unit tests for the AAR processor system.

## Test Structure

- `test_database_manager.py` - Database operations and persistence
- `test_monitoring_integration.py` - Monitoring and observability integration
- `test_aar_generator.py` - AAR generation and report creation
- `test_sacred_geometry_engine.py` - Sacred Geometry validation and compliance
- `test_compliance_checker.py` - Compliance validation and scoring
- `test_aar_processor.py` - Main API endpoints and FastAPI integration
- `conftest.py` - Test configuration and shared fixtures
- `test_integration.py` - End-to-end integration tests

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_database_manager.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html -v

# Run integration tests only
python -m pytest tests/test_integration.py -v
```

## Test Coverage Goals

- Database operations: 100%
- Monitoring integration: 95%
- AAR generation: 95%
- Sacred Geometry engine: 100%
- API endpoints: 90%
- Integration flows: 85%
