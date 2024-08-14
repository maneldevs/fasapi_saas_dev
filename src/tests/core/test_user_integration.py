from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import User, UserCreateCommand, UserUpdateCommand


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


def test_id_read_index_happy(client: TestClient, users_in_db: list[User]):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == users_in_db[0].id
    assert data[0]["username"] == users_in_db[0].username
    assert data[1]["id"] == users_in_db[1].id
    assert data[1]["username"] == users_in_db[1].username


def test_id_read_index_none_in_db(client: TestClient):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


""" Read by id """


def test_id_read_by_id_happy(client: TestClient, user_in_db: User):
    response = client.get(f"{BASE_URL}/{user_in_db.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == user_in_db.id
    assert data["username"] == user_in_db.username
    assert data["firstname"] == user_in_db.firstname
    assert data["lastname"] == user_in_db.lastname
    assert data["active"] == user_in_db.active
    assert data["is_god"] == user_in_db.is_god
    assert data["role"]["id"] == user_in_db.role.id
    assert data["role"]["code"] == user_in_db.role.code
    assert data["role"]["webname"] == user_in_db.role.webname
    assert data["group"]["id"] == user_in_db.group.id
    assert data["group"]["code"] == user_in_db.group.code
    assert data["group"]["webname"] == user_in_db.group.webname
    assert data["group"]["active"] == user_in_db.group.active


def test_id_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


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


def test_i_update_group_happy(
    client: TestClient, session: Session, user_update_command: UserUpdateCommand, user_in_db: User
):
    body = user_update_command.model_dump()
    original_encoded_password = user_in_db.password
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    data = response.json()
    user_updated = session.get(User, {data["id"]})
    assert user_updated is not None
    assert response.status_code == 200
    assert data["id"] == user_updated.id
    assert data["username"] == user_updated.username
    assert data["firstname"] == user_updated.firstname
    assert data["lastname"] == user_updated.lastname
    assert data["active"] == user_updated.active
    assert data["is_god"] == user_updated.is_god
    assert data["group"]["id"] == user_updated.group_id
    assert data["group"]["code"] == user_updated.group.code
    assert data["group"]["webname"] == user_updated.group.webname
    assert data["group"]["active"] == user_updated.group.active
    assert data["role"]["id"] == user_updated.role_id
    assert data["role"]["code"] == user_updated.role.code
    assert data["role"]["webname"] == user_updated.role.webname
    assert user_updated.id == user_in_db.id
    assert user_updated.username == user_update_command.username
    assert user_updated.password != original_encoded_password
    assert user_updated.firstname == user_update_command.firstname
    assert user_updated.lastname == user_update_command.lastname
    assert user_updated.active == user_update_command.active
    assert user_updated.is_god == user_update_command.is_god
    assert user_updated.group.id == user_update_command.group_id
    assert user_updated.group.id == user_update_command.role_id


def test_i_update_no_password(
    client: TestClient, session: Session, user_update_command: UserUpdateCommand, user_in_db: User
):
    user_update_command.password_raw = None
    body = user_update_command.model_dump()
    original_encoded_password = user_in_db.password
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    data = response.json()
    user_updated = session.get(User, {data["id"]})
    assert user_updated is not None
    assert response.status_code == 200
    assert data["id"] == user_updated.id
    assert data["username"] == user_updated.username
    assert user_updated.id == user_in_db.id
    assert user_updated.username == user_update_command.username
    assert user_updated.password == original_encoded_password


def test_i_update_no_username(client: TestClient, user_update_command: UserUpdateCommand, user_in_db: User):
    user_update_command.username = None
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_active(client: TestClient, user_update_command: UserUpdateCommand, user_in_db: User):
    user_update_command.active = None
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_is_god(client: TestClient, user_update_command: UserUpdateCommand, user_in_db: User):
    user_update_command.is_god = None
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_group_id(
    client: TestClient, session: Session, user_update_command: UserUpdateCommand, user_in_db: User
):
    user_update_command.group_id = None
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    data = response.json()
    user_updated = session.get(User, {data["id"]})
    assert response.status_code == 200
    assert data["group"] is None
    assert user_updated.group is None


def test_i_update_no_role_id(
    client: TestClient, session: Session, user_update_command: UserUpdateCommand, user_in_db: User
):
    user_update_command.role_id = None
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    data = response.json()
    user_updated = session.get(User, {data["id"]})
    assert response.status_code == 200
    assert data["role"] is None
    assert user_updated.role is None


def test_i_update_no_existent_user(client: TestClient, user_update_command: UserUpdateCommand):
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


def test_i_update_no_existent_group_id(client: TestClient, user_update_command: UserUpdateCommand, user_in_db: User):
    user_update_command.group_id = "nonexistent"
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    assert response.status_code == 404


def test_i_update_no_existent_role_id(client: TestClient, user_update_command: UserUpdateCommand, user_in_db: User):
    user_update_command.role_id = "nonexistent"
    body = user_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{user_in_db.id}", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_group_happy(client: TestClient, session: Session, user_in_db: User):
    response = client.delete(f"{BASE_URL}/{user_in_db.id}")
    group_in_db_after = session.get(User, user_in_db.id)
    assert response.status_code == 204
    assert group_in_db_after is None


def test_i_delete_group_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404
