from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import Role, RoleCommand

BASE_URL: str = "/api/core/roles"


""" Read """


def test_id_read_paginated_happy(client: TestClient, roles_in_db: list[Role]):
    params = {"page": 2, "size": 1, "order_field": "code", "direction": "desc"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert data["page"] == 2
    assert data["size"] == 1
    assert data["total"] == 2
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == roles_in_db[0].id
    assert data["content"][0]["code"] == roles_in_db[0].code
    assert data["content"][0]["webname"] == roles_in_db[0].webname


def test_id_read_filtered_happy(client: TestClient, roles_in_db: list[Role]):
    params = {"target": "role1"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == roles_in_db[0].id
    assert data["content"][0]["code"] == roles_in_db[0].code
    assert data["content"][0]["webname"] == roles_in_db[0].webname


def test_id_read_none_no_params(client: TestClient, roles_in_db: list[Role]):
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


def test_id_read_index_happy(client: TestClient, roles_in_db: list[Role]):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["code"] == roles_in_db[0].code
    assert data[0]["webname"] == roles_in_db[0].webname
    assert data[0]["id"] == roles_in_db[0].id
    assert data[1]["code"] == roles_in_db[1].code
    assert data[1]["webname"] == roles_in_db[1].webname
    assert data[1]["id"] == roles_in_db[1].id


def test_id_read_index_none_in_db(client: TestClient):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


""" Read by id """


def test_id_read_by_id_happy(client: TestClient, role_in_db: Role):
    response = client.get(f"{BASE_URL}/{role_in_db.id}")
    data = response.json()
    assert data["code"] == role_in_db.code
    assert data["webname"] == role_in_db.webname
    assert data["id"] == role_in_db.id


def test_id_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Create """


def test_i_create_group_happy(client: TestClient, session: Session, role_command: RoleCommand):
    body = role_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    group_created = session.get(Role, {data["id"]})
    assert response.status_code == 201
    assert group_created is not None
    assert data["code"] == role_command.code
    assert data["webname"] == role_command.webname
    assert data["id"] is not None
    assert data["code"] == group_created.code
    assert data["webname"] == group_created.webname
    assert data["id"] == group_created.id


def test_i_create_group_no_code(client: TestClient, role_command: RoleCommand):
    role_command.code = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_group_no_webname(client: TestClient, role_command: RoleCommand):
    role_command.webname = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


""" Update """


def test_i_update_group_happy(client: TestClient, session: Session, role_command: RoleCommand, role_in_db: Role):
    body = role_command.model_dump()
    response = client.put(f"{BASE_URL}/{role_in_db.id}", json=body)
    data = response.json()
    group_updated = session.get(Role, {data["id"]})
    assert group_updated is not None
    assert response.status_code == 200
    assert data["code"] == role_command.code
    assert data["webname"] == role_command.webname
    assert data["id"] == role_in_db.id
    assert data["code"] == group_updated.code
    assert data["webname"] == group_updated.webname
    assert data["id"] == group_updated.id


def test_i_update_group_no_code(client: TestClient, role_command: RoleCommand, role_in_db: Role):
    role_command.code = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{role_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_group_no_webname(client: TestClient, role_command: RoleCommand, role_in_db: Role):
    role_command.webname = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{role_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_group_no_existent(client: TestClient, role_command: RoleCommand):
    body = role_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_group_happy(client: TestClient, session: Session, role_in_db: Role):
    response = client.delete(f"{BASE_URL}/{role_in_db.id}")
    group_in_db_after = session.get(Role, role_in_db.id)
    assert response.status_code == 204
    assert group_in_db_after is None


def test_i_delete_group_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404