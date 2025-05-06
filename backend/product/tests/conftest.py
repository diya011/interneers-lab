import pytest
from mongoengine import connect, disconnect
from seed_data.clear_database import clear_database

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Set up the test MongoDB database once per test session."""
    disconnect(alias="default")  # Disconnect any existing default connection
    connect(
        db="productDB_test",   # YOUR test database name
        host="mongodb://localhost:27017/productDB_test",
        alias="default"
    )
    yield
    clear_database()
    disconnect()

@pytest.fixture(autouse=True)
def reset_db():
    """Clear the database after each test."""
    clear_database()
