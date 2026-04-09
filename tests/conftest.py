"""
Pytest configuration and fixtures for integration tests.

This module provides fixtures that simulate real-world scenarios
like database connections, external API calls, and file operations.
"""

import pytest
import time
from typing import Generator


@pytest.fixture(scope="session")
def simulated_database_connection():
    """
    Simulate database connection setup/teardown.
    In real scenarios, this would connect to a test database.
    """
    # Simulate connection time
    time.sleep(0.1)
    print("\n🔌 Database connection established")

    yield {"status": "connected", "pool_size": 10}

    # Simulate cleanup
    time.sleep(0.05)
    print("\n🔌 Database connection closed")


@pytest.fixture(scope="function")
def simulated_external_nutrition_api():
    """
    Simulate calls to external nutrition database API.
    In real scenarios, this would fetch food data from external services.
    """
    def fetch_nutrition_data(food_name: str):
        # Simulate API latency
        time.sleep(0.03)
        return {
            "name": food_name,
            "calories": 100,
            "protein": 10,
            "carbs": 15,
            "fat": 5
        }

    return fetch_nutrition_data


@pytest.fixture(scope="function")
def simulated_user_profile_cache():
    """
    Simulate a cache layer for user profiles.
    In real scenarios, this would be Redis or Memcached.
    """
    cache = {}

    def get_or_set(key: str, value_func):
        if key not in cache:
            # Simulate cache miss and fetch from "database"
            time.sleep(0.02)
            cache[key] = value_func()
        return cache[key]

    return get_or_set


@pytest.fixture(scope="function")
def simulated_file_storage():
    """
    Simulate file storage operations (S3, local disk, etc.).
    In real scenarios, this would save/load workout plans to storage.
    """
    storage = {}

    class FileStorage:
        def save(self, filename: str, content: dict):
            # Simulate disk I/O
            time.sleep(0.02)
            storage[filename] = content
            return {"status": "saved", "path": f"/storage/{filename}"}

        def load(self, filename: str):
            # Simulate disk read
            time.sleep(0.02)
            return storage.get(filename)

    return FileStorage()


@pytest.fixture(scope="function")
def simulated_email_service():
    """
    Simulate email service for sending workout plans.
    In real scenarios, this would use SendGrid, AWS SES, etc.
    """
    sent_emails = []

    def send_email(to: str, subject: str, body: str):
        # Simulate email API call
        time.sleep(0.05)
        email = {
            "to": to,
            "subject": subject,
            "body": body,
            "sent_at": time.time()
        }
        sent_emails.append(email)
        return {"status": "sent", "message_id": f"msg_{len(sent_emails)}"}

    send_email.sent = sent_emails
    return send_email


@pytest.fixture(autouse=True, scope="function")
def reset_test_state():
    """
    Automatically reset state between tests.
    Simulates clearing caches, resetting connections, etc.
    """
    # Setup
    yield
    # Teardown - simulate cleanup operations
    pass


# Markers for test categorization
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers",
        "integration: mark test as integration test (multiple components)"
    )
    config.addinivalue_line(
        "markers",
        "slow: mark test as slow running (> 0.5s)"
    )
    config.addinivalue_line(
        "markers",
        "unit: mark test as unit test (fast, isolated)"
    )


def pytest_collection_modifyitems(config, items):
    """
    Automatically add markers to tests based on their names/locations.
    """
    for item in items:
        # Add 'unit' marker to tests in test_*.py files (except test_integration.py)
        if "test_integration" not in item.nodeid:
            if "integration" not in [mark.name for mark in item.iter_markers()]:
                item.add_marker(pytest.mark.unit)
