"""
Basic tests for E-Commerce Platform
"""
import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("config.DevConfig")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_home_page(client):
    """Test home page loads."""
    response = client.get("/")
    assert response.status_code == 200


def test_register_page(client):
    """Test register page loads."""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_login_page(client):
    """Test login page loads."""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_products_page(client):
    """Test products page loads."""
    response = client.get("/products")
    assert response.status_code == 200


def test_cart_requires_login(client):
    """Test cart page requires authentication."""
    response = client.get("/cart", follow_redirects=True)
    # Should redirect to login
    assert response.status_code == 200
    assert b"Login" in response.data or b"log in" in response.data.lower()


def test_admin_requires_login(client):
    """Test admin dashboard requires authentication."""
    response = client.get("/admin/dashboard", follow_redirects=True)
    # Should redirect to login
    assert response.status_code == 200
    assert b"Login" in response.data or b"log in" in response.data.lower()

