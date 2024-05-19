import pytest
import httpx
from fastapi.testclient import TestClient
from StarterFastAPIUserLogin.api.server import app, create_jwt_token, \
    authenticate_user  # Adjust the import according to your actual file structure
from StarterFastAPIUserLogin.models.users import User
from datetime import datetime
from pydantic import EmailStr
import bcrypt
import json

client = TestClient(app)


@pytest.fixture
def test_user():
    password = "password123"
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode('utf-8')

    user = User(
        username="testuser",
        password_hash=hashed_password,
        created=datetime.utcnow(),
        email=EmailStr("testuser@example.com"),
        profile_image_s3_path=None,
        bio="Test user bio",
        last_login=None,
        is_active=True,
        is_admin=False,
        date_of_birth=None,
        phone_number=None
    )
    return user, password


@pytest.fixture
def setup_user(test_user):
    user, _ = test_user
    with Client(config) as client:
        try:
            client.insert_user(user)
        except Exception as e:
            print(f"Error setting up user: {e}")


def test_create_user():
    response = client.post("/user/create", json={
        "username": "newuser",
        "password": "newpassword123",
        "email": "newuser@example.com"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "success"}


def test_login(setup_user, test_user):
    _, password = test_user
    response = client.post("/login/", data={
        "username": "testuser",
        "password": password
    })
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"


if __name__ == "__main__":
    pytest.main()
