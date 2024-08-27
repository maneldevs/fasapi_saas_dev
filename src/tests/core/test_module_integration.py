from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import Module, ModuleCommand


BASE_URL: str = "/api/core/modules"


""" Read """


def test_id_read_paginated_happy(client: TestClient, modules_in_db: list[Module]):
    params = {"page": 2, "size": 1, "order_field": "code", "direction": "desc"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert data["page"] == 2
    assert data["size"] == 1
    assert data["total"] == 2
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == modules_in_db[0].id
    assert data["content"][0]["code"] == modules_in_db[0].code
    assert data["content"][0]["webname"] == modules_in_db[0].webname


def test_id_read_filtered_happy(client: TestClient, modules_in_db: list[Module]):
    params = {"target": "module1"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == modules_in_db[0].id
    assert data["content"][0]["code"] == modules_in_db[0].code
    assert data["content"][0]["webname"] == modules_in_db[0].webname


def test_id_read_none_no_params(client: TestClient, modules_in_db: list[Module]):
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


def test_id_read_index_happy(client: TestClient, modules_in_db: list[Module]):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["code"] == modules_in_db[0].code
    assert data[0]["webname"] == modules_in_db[0].webname
    assert data[0]["id"] == modules_in_db[0].id
    assert data[1]["code"] == modules_in_db[1].code
    assert data[1]["webname"] == modules_in_db[1].webname
    assert data[1]["id"] == modules_in_db[1].id


def test_id_read_index_none_in_db(client: TestClient):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


""" Read by id """


def test_id_read_by_id_happy(client: TestClient, module_in_db: Module):
    response = client.get(f"{BASE_URL}/{module_in_db.id}")
    data = response.json()
    assert data["code"] == module_in_db.code
    assert data["webname"] == module_in_db.webname
    assert data["id"] == module_in_db.id


def test_id_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Create """


def test_i_create_happy(client: TestClient, session: Session, module_command: ModuleCommand):
    body = module_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    created = session.get(Module, {data["id"]})
    assert response.status_code == 201
    assert created is not None
    assert data["code"] == module_command.code
    assert data["webname"] == module_command.webname
    assert data["id"] is not None
    assert data["code"] == created.code
    assert data["webname"] == created.webname
    assert data["id"] == created.id


def test_i_create_no_code(client: TestClient, module_command: ModuleCommand):
    module_command.code = None
    body = module_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_no_webname(client: TestClient, module_command: ModuleCommand):
    module_command.webname = None
    body = module_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


""" Update """


def test_i_update_happy(client: TestClient, session: Session, module_command: ModuleCommand, module_in_db: Module):
    body = module_command.model_dump()
    response = client.put(f"{BASE_URL}/{module_in_db.id}", json=body)
    data = response.json()
    module_updated = session.get(Module, {data["id"]})
    assert module_updated is not None
    assert response.status_code == 200
    assert data["code"] == module_command.code
    assert data["webname"] == module_command.webname
    assert data["id"] == module_in_db.id
    assert data["code"] == module_updated.code
    assert data["webname"] == module_updated.webname
    assert data["id"] == module_updated.id


def test_i_update_no_code(client: TestClient, module_command: ModuleCommand, module_in_db: Module):
    module_command.code = None
    body = module_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{module_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_webname(client: TestClient, module_command: ModuleCommand, module_in_db: Module):
    module_command.webname = None
    body = module_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{module_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_existent(client: TestClient, module_command: ModuleCommand):
    body = module_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_happy(client: TestClient, session: Session, module_in_db: Module):
    response = client.delete(f"{BASE_URL}/{module_in_db.id}")
    module_in_db_after = session.get(Module, module_in_db.id)
    assert response.status_code == 204
    assert module_in_db_after is None


def test_i_delete_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404
