from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import User, UserCreateCommand


BASE_URL: str = "/api/core/users"

""" Read """


""" Read index """


""" Read by id """


""" Read by username """


""" Create """


def test_i_create_user_happy(client: TestClient, session: Session, user_create_command: UserCreateCommand):
    body = user_create_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    created = session.get(User, data["id"])

    assert response.status_code == 201
    assert created is not None

    assert data["username"] == user_create_command.username
    assert data["firstname"] == user_create_command.firstname
    assert data["lastname"] == user_create_command.lastname
    assert data["active"] is True
    assert data["is_god"] is False
    assert data["id"] is not None
    assert data["role"]["id"] == user_create_command.role_id
    assert data["group"]["id"] == user_create_command.group_id

    assert data["username"] == created.username
    assert data["firstname"] == created.firstname
    assert data["lastname"] == created.lastname
    assert data["active"] == created.active
    assert data["is_god"] == created.is_god
    assert data["id"] == created.id
    assert data["group"]["code"] == created.group.code
    assert data["group"]["webname"] == created.group.webname
    assert data["group"]["active"] == created.group.active
    assert data["group"]["id"] == created.group.id
    assert data["role"]["code"] == created.role.code
    assert data["role"]["webname"] == created.role.webname
    assert data["group"]["id"] == created.role.id


def test_i_create_user_no_username(client: TestClient, user_create_command: UserCreateCommand):
    user_create_command.username = None
    body = user_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_user_no_password(client: TestClient, user_create_command: UserCreateCommand):
    user_create_command.password_raw = None
    body = user_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_user_with_non_existent_role(client: TestClient, user_create_command: UserCreateCommand):
    user_create_command.role_id = "nonexistent"
    body = user_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 404


def test_i_create_user_with_non_existent_group(client: TestClient, user_create_command: UserCreateCommand):
    user_create_command.group_id = "nonexistent"
    body = user_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 404


def test_i_create_user_already_existent(client: TestClient, user_create_command: UserCreateCommand, user_in_db: User):
    user_create_command.username = user_in_db.username
    body = user_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 400


""" Update """


""" Delete """
