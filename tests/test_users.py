import pytest
from app import schemas
from fastapi import status
from app.config import settings
from jose import jwt

def test_create_user(client):
    res = client.post("/users/", json={"email": "meowmeowCat@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "meowmeowCat@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_201_CREATED
