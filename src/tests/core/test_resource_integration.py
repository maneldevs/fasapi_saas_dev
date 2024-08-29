from fastapi.testclient import TestClient
from sqlmodel import Session
from src.app.modules.core.domain.models import Resource, ResourceUpdateCommand

BASE_URL: str = "/api/core/resources"


""" Read by id """


def test_i_read_by_id_happy(client: TestClient, resource_in_db: Resource):
    response = client.get(f"{BASE_URL}/{resource_in_db.id}")
    data = response.json()
    assert data["id"] == resource_in_db.id
    assert data["code"] == resource_in_db.code
    assert data["module"]["id"] == resource_in_db.module.id
    assert data["module"]["code"] == resource_in_db.module.code
    assert data["module"]["webname"] == resource_in_db.module.webname


def test_i_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Update """


def test_i_update_happy(
    client: TestClient, session: Session, resource_update_command: ResourceUpdateCommand, resource_in_db: Resource
):
    body = resource_update_command.model_dump()
    response = client.put(f"{BASE_URL}/{resource_in_db.id}", json=body)
    data = response.json()
    resource_updated = session.get(Resource, {data["id"]})
    assert resource_updated is not None
    assert response.status_code == 200
    assert data["id"] == resource_in_db.id
    assert data["code"] == resource_update_command.code == resource_in_db.code
    assert data["module"]["id"] == resource_update_command.module_id == resource_in_db.module.id
    assert data["module"]["code"] == resource_in_db.module.code
    assert data["module"]["webname"] == resource_in_db.module.webname


def test_i_update_no_code(client: TestClient, resource_update_command: ResourceUpdateCommand, resource_in_db: Resource):
    resource_update_command.code = None
    body = resource_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{resource_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_module_id(
    client: TestClient, resource_update_command: ResourceUpdateCommand, resource_in_db: Resource
):
    resource_update_command.module_id = None
    body = resource_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{resource_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_module_id_no_exists(
    client: TestClient, resource_update_command: ResourceUpdateCommand, resource_in_db: Resource
):
    resource_update_command.module_id = "8888"
    body = resource_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{resource_in_db.id}", json=body)
    assert response.status_code == 404


def test_i_update_no_existent(client: TestClient, resource_update_command: ResourceUpdateCommand):
    body = resource_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_happy(client: TestClient, session: Session, resource_in_db: Resource):
    response = client.delete(f"{BASE_URL}/{resource_in_db.id}")
    module_in_db_after = session.get(Resource, resource_in_db.id)
    assert response.status_code == 204
    assert module_in_db_after is None


def test_i_delete_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404
