"""
Intentionally failing tests for Smart Tests verification.

These tests are designed to fail to:
1. Verify Smart Tests records test failures correctly
2. Test CI/CD pipeline failure handling
3. See how Smart Tests learns from failures
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_intentional_failure_assertion():
    """This test will always fail - assertion error."""
    assert 1 == 2, "Intentional failure: 1 does not equal 2"


def test_intentional_failure_calculation():
    """This test will fail due to incorrect calculation."""
    result = 5 + 5
    assert result == 11, f"Expected 11 but got {result}"


def test_intentional_failure_api_response():
    """This test expects wrong response from API."""
    response = client.get("/")
    assert response.status_code == 404, "Expected 404 but API returned 200"


def test_intentional_failure_value_error():
    """This test will fail with ValueError."""
    value = "not a number"
    result = int(value)  # This will raise ValueError
    assert result == 42


def test_intentional_failure_type_check():
    """This test will fail due to type mismatch."""
    response = client.get("/health")
    data = response.json()
    # Expecting int but it's a string
    assert isinstance(data["status"], int), "Status should be int but it's a string"


@pytest.mark.parametrize("weight,height,expected_bmi", [
    (70, 175, 99.99),  # Wrong expectation - will fail
    (80, 180, 88.88),  # Wrong expectation - will fail
])
def test_intentional_failure_parametrized(weight, height, expected_bmi):
    """Parametrized test that will fail for all parameters."""
    response = client.post(f"/calculate/bmi?weight_kg={weight}&height_cm={height}")
    assert response.status_code == 200
    data = response.json()
    # These BMI values are intentionally wrong
    assert data["bmi"] == expected_bmi, f"Expected {expected_bmi} but got {data['bmi']}"
