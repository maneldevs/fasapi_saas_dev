from fastapi.testclient import TestClient
from sqlmodel import Session
from src.app.modules.core.domain.models import Permission, PermissionUpdateCommand

BASE_URL: str = "/api/core/permissions"


""" Read by id """


def test_i_read_by_id_happy(client: TestClient, permission_in_db: Permission):
    response = client.get(f"{BASE_URL}/{permission_in_db.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == permission_in_db.id
    assert data["scope"] == permission_in_db.scope
    assert data["scope_owner"] == permission_in_db.scope_owner
    assert data["resource"]["id"] == permission_in_db.resource.id
    assert data["resource"]["code"] == permission_in_db.resource.code
    assert data["resource"]["module"]["id"] == permission_in_db.resource.module.id
    assert data["resource"]["module"]["code"] == permission_in_db.resource.module.code
    assert data["resource"]["module"]["webname"] == permission_in_db.resource.module.webname
    assert data["role"]["id"] == permission_in_db.role.id
    assert data["role"]["code"] == permission_in_db.role.code
    assert data["role"]["webname"] == permission_in_db.role.webname


def test_i_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


# """ Update """


def test_i_update_happy(
    client: TestClient,
    session: Session,
    permission_update_command: PermissionUpdateCommand,
    permission_in_db: Permission,
):
    body = permission_update_command.model_dump()
    response = client.put(f"{BASE_URL}/{permission_in_db.id}", json=body)
    data = response.json()
    updated = session.get(Permission, {data["id"]})
    assert updated is not None
    assert response.status_code == 200
    assert data["id"] == updated.id
    assert data["scope"] == permission_update_command.scope == updated.scope
    assert data["scope_owner"] == permission_update_command.scope_owner == updated.scope_owner
    assert data["resource"]["id"] == updated.resource.id
    assert data["resource"]["code"] == updated.resource.code
    assert data["resource"]["module"]["id"] == updated.resource.module.id
    assert data["resource"]["module"]["code"] == updated.resource.module.code
    assert data["resource"]["module"]["webname"] == updated.resource.module.webname
    assert data["role"]["id"] == updated.role.id
    assert data["role"]["code"] == updated.role.code
    assert data["role"]["webname"] == updated.role.webname


def test_i_update_no_scope_happy(
    client: TestClient,
    session: Session,
    permission_update_command: PermissionUpdateCommand,
    permission_in_db: Permission,
):
    permission_update_command.scope = None
    body = permission_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{permission_in_db.id}", json=body)
    data = response.json()
    updated = session.get(Permission, {data["id"]})
    assert response.status_code == 200
    assert updated is not None
    assert data["scope"] is None


def test_i_update_no_existent(client: TestClient, permission_update_command: PermissionUpdateCommand):
    body = permission_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_happy(client: TestClient, session: Session, permission_in_db: Permission):
    response = client.delete(f"{BASE_URL}/{permission_in_db.id}")
    module_in_db_after = session.get(Permission, permission_in_db.id)
    assert response.status_code == 204
    assert module_in_db_after is None


def test_i_delete_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404
