from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import User, UserCreateCommand


BASE_URL: str = "/api/core/users"


""" Read """


def test_id_read_paginated_happy(client: TestClient, users_in_db: list[User]):
    params = {"page": 2, "size": 1, "order_field": "username", "direction": "desc"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert data["page"] == 2
    assert data["size"] == 1
    assert data["total"] == 2
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == users_in_db[0].id
    assert data["content"][0]["username"] == users_in_db[0].username
    assert data["content"][0]["firstname"] == users_in_db[0].firstname
    assert data["content"][0]["lastname"] == users_in_db[0].lastname
    assert data["content"][0]["active"] == users_in_db[0].active
    assert data["content"][0]["is_god"] == users_in_db[0].is_god
    assert data["content"][0]["role"]["id"] == users_in_db[0].role.id
    assert data["content"][0]["role"]["code"] == users_in_db[0].role.code
    assert data["content"][0]["role"]["webname"] == users_in_db[0].role.webname
    assert data["content"][0]["group"]["id"] == users_in_db[0].group.id
    assert data["content"][0]["group"]["code"] == users_in_db[0].group.code
    assert data["content"][0]["group"]["webname"] == users_in_db[0].group.webname
    assert data["content"][0]["group"]["active"] == users_in_db[0].group.active


def test_id_read_filtered_by_multiple_params_happy(client: TestClient, users_in_db: list[User]):
    group_id = users_in_db[0].group_id
    params = {"target": "u", "active": True, "is_god": False, "group_id": group_id}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 2


def test_id_read_filtered_by_multiple_params_no_matches(client: TestClient, users_in_db: list[User]):
    group_id = "nonexistent"
    params = {"target": "u", "active": True, "is_god": False, "group_id": group_id}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 0


def test_id_read_filtered_by_target_happy(client: TestClient, users_in_db: list[User]):
    params = {"target": "my"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == users_in_db[0].id


def test_id_read_filtered_by_target_no_matches(client: TestClient, users_in_db: list[User]):
    params = {"target": "."}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 0


def test_id_read_filtered_by_group_id_happy(client: TestClient, users_in_db: list[User]):
    group_id = users_in_db[0].group_id
    params = {"group_id": group_id}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 2


def test_id_read_filtered_by_group_id_no_matches(client: TestClient, users_in_db: list[User]):
    group_id = "non_existent"
    params = {"group_id": group_id}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 0


def test_id_read_filtered_by_active_happy(client: TestClient, users_in_db: list[User]):
    params = {"active": True}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 2


def test_id_read_filtered_by_active_no_matches(client: TestClient, users_in_db: list[User]):
    params = {"active": False}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 0


def test_id_read_filtered_by_is_god_happy(client: TestClient, users_in_db: list[User]):
    params = {"is_god": False}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 2


def test_id_read_filtered_by_is_god_no_matches(client: TestClient, users_in_db: list[User]):
    params = {"is_god": True}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 0


def test_id_read_no_params(client: TestClient, users_in_db: list[User]):
    response = client.get(f"{BASE_URL}")
    data = response.json()
    assert data["page"] == 1
    assert data["size"] == 10
    assert data["total"] == 2
    assert len(data["content"]) == 2


def test_id_read_none_in_db(client: TestClient):
    response = client.get(f"{BASE_URL}")
    data = response.json()
    assert len(data["content"]) == 0


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
