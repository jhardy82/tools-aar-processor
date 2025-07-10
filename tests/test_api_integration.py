"""
🌐 Sacred Geometry AAR Processor - API Integration Tests
Tests the FastAPI endpoints and complete workflows
"""

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
from src.aar_processor import app


class TestAARProcessorAPI:
    """Integration tests for the AAR Processor FastAPI application"""

    @pytest.fixture
    def client(self):
        """Create test client for FastAPI app"""
        return TestClient(app)

    def test_health_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "sacred_geometry" in data
        assert data["sacred_geometry"]["phi"] == pytest.approx(
            1.618033988749895, rel=1e-10
        )

    def test_generate_aar_endpoint(self, client):
        """Test AAR generation endpoint"""
        # Test data following the AARRequest model
        aar_request = {
            "mission_id": "api_test_001",
            "mission_type": "integration_test",
            "start_time": "2025-06-18T23:00:00Z",
            "end_time": "2025-06-18T23:30:00Z",
            "participants": ["user1", "user2"],
            "objectives": ["Test API integration", "Validate Sacred Geometry patterns"],
            "outcomes": ["API working correctly", "Sacred Geometry validated"],
            "lessons_learned": ["Integration tests are crucial", "API design is solid"],
            "metadata": {"test_run": True, "integration": "api_test"},
        }

        response = client.post("/aar/generate", json=aar_request)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "accepted"
        assert "aar_id" in data
        assert data["message"] == "AAR generation started"

        # Verify AAR ID follows Sacred Geometry pattern (hexadecimal with golden ratio)
        aar_id = data["aar_id"]
        assert len(aar_id) == 32  # Should be 32-character hex string
        assert all(c in "0123456789abcdef" for c in aar_id)

    def test_get_aar_status_endpoint(self, client):
        """Test AAR status retrieval endpoint"""
        # First create an AAR
        aar_request = {
            "mission_id": "status_test_001",
            "mission_type": "status_check",
            "start_time": "2025-06-18T23:00:00Z",
            "end_time": "2025-06-18T23:15:00Z",
            "participants": ["test_user"],
            "objectives": ["Test status endpoint"],
            "outcomes": ["Status retrieved successfully"],
            "lessons_learned": ["Status endpoints work well"],
        }

        # Generate AAR
        gen_response = client.post("/aar/generate", json=aar_request)
        assert gen_response.status_code == 200
        aar_id = gen_response.json()["aar_id"]

        # Give it a moment to process (in real implementation, this would be async)
        import time

        time.sleep(0.1)

        # Check status
        status_response = client.get(f"/aar/{aar_id}/status")

        # Could be 200 (found) or 404 (not found yet), both are valid for async processing
        if status_response.status_code == 200:
            data = status_response.json()
            assert "aar_id" in data
            assert data["aar_id"] == aar_id
        elif status_response.status_code == 404:
            # This is fine for async processing - AAR might still be processing
            assert "not found" in status_response.json().get("detail", "").lower()

    def test_get_aar_report_endpoint(self, client):
        """Test AAR report retrieval endpoint"""
        # Test with a non-existent AAR ID first
        response = client.get("/aar/nonexistent_id/report")
        assert response.status_code == 404

    def test_compliance_status_endpoint(self, client):
        """Test compliance status endpoint"""
        response = client.get("/compliance/status")
        assert response.status_code == 200

        data = response.json()
        assert "current_compliance_score" in data
        assert "sacred_geometry_patterns" in data
        assert "timestamp" in data

        # Verify compliance score is valid
        score = data["current_compliance_score"]
        assert 0.0 <= score <= 1.0

    def test_sacred_geometry_validation_endpoint(self, client):
        """Test Sacred Geometry data validation endpoint"""
        # Test valid data
        valid_data = {
            "objectives": ["Implement circle pattern", "Create triangular stability"],
            "outcomes": ["Circle completed", "Triangle validated"],
            "metrics": {"completion_rate": 0.85, "quality_score": 0.92},
        }

        response = client.post("/sacred-geometry/validate", json=valid_data)
        assert response.status_code == 200

        data = response.json()
        assert "is_valid" in data
        assert "patterns_detected" in data
        assert "sacred_geometry_score" in data

    def test_metrics_endpoint(self, client):
        """Test Prometheus metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200

        # Should return Prometheus format
        content = response.text
        assert "aar_requests_total" in content or "# HELP" in content

    def test_cors_headers(self, client):
        """Test CORS headers are properly set"""
        response = client.options("/health")
        # CORS should be configured based on the middleware setup

    def test_error_handling(self, client):
        """Test API error handling"""
        # Test invalid JSON
        response = client.post("/aar/generate", data="invalid json")
        assert response.status_code == 422  # Unprocessable Entity

        # Test missing required fields
        invalid_request = {"mission_id": "test"}  # Missing required fields
        response = client.post("/aar/generate", json=invalid_request)
        assert response.status_code == 422

    def test_concurrent_requests(self, client):
        """Test handling of concurrent AAR requests"""
        import threading

        results = []

        def make_request(i):
            aar_request = {
                "mission_id": f"concurrent_test_{i}",
                "mission_type": "concurrency_test",
                "start_time": "2025-06-18T23:00:00Z",
                "end_time": "2025-06-18T23:15:00Z",
                "participants": [f"user_{i}"],
                "objectives": [f"Concurrent test {i}"],
                "outcomes": [f"Request {i} processed"],
                "lessons_learned": [f"Concurrency test {i} completed"],
            }

            response = client.post("/aar/generate", json=aar_request)
            results.append((i, response.status_code, response.json()))

        # Create multiple threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=make_request, args=(i,))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Verify all requests succeeded
        assert len(results) == 5
        for i, status_code, data in results:
            assert status_code == 200, f"Request {i} failed with status {status_code}"
            assert "aar_id" in data


class TestIntegrationWorkflows:
    """Integration tests for complete workflows"""

    @pytest.fixture
    def client(self):
        """Create test client for FastAPI app"""
        return TestClient(app)

    def test_complete_aar_workflow(self, client):
        """Test complete AAR processing workflow through API"""
        # Step 1: Generate AAR
        aar_request = {
            "mission_id": "workflow_test_001",
            "mission_type": "complete_workflow",
            "start_time": "2025-06-18T23:00:00Z",
            "end_time": "2025-06-18T23:45:00Z",
            "participants": ["lead_user", "support_user"],
            "objectives": [
                "Test complete workflow",
                "Validate all integrations",
                "Ensure Sacred Geometry compliance",
            ],
            "outcomes": [
                "Workflow completed successfully",
                "All integrations validated",
                "Sacred Geometry patterns detected",
            ],
            "lessons_learned": [
                "Complete workflows provide best validation",
                "Integration testing is essential",
                "Sacred Geometry adds valuable insights",
            ],
            "metadata": {
                "priority": "high",
                "category": "integration_test",
                "golden_ratio_section": 39,  # φ³ section
            },
        }

        # Generate AAR
        response = client.post("/aar/generate", json=aar_request)
        assert response.status_code == 200
        aar_id = response.json()["aar_id"]

        # Step 2: Check compliance status
        compliance_response = client.get("/compliance/status")
        assert compliance_response.status_code == 200

        # Step 3: Validate Sacred Geometry
        sg_response = client.post(
            "/sacred-geometry/validate",
            json={
                "objectives": aar_request["objectives"],
                "outcomes": aar_request["outcomes"],
            },
        )
        assert sg_response.status_code == 200

        # Step 4: Check health
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"

    def test_error_recovery_workflow(self, client):
        """Test error handling and recovery in workflows"""
        # Test with intentionally problematic data
        problematic_request = {
            "mission_id": "",  # Empty mission ID
            "mission_type": "error_test",
            "start_time": "invalid_time",  # Invalid timestamp
            "end_time": "2025-06-18T23:00:00Z",
            "participants": [],  # Empty participants
            "objectives": [],  # Empty objectives
            "outcomes": [],  # Empty outcomes
            "lessons_learned": [],  # Empty lessons
        }

        response = client.post("/aar/generate", json=problematic_request)
        # Should handle gracefully with appropriate error response
        assert response.status_code in [400, 422]  # Bad Request or Unprocessable Entity


if __name__ == "__main__":
    # Run API integration tests
    pytest.main([__file__, "-v"])
