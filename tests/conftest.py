import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def app_context():
    """Create an application context."""
    with app.app_context():
        yield app