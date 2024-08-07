from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import Group, GroupCreateCommand, GroupUpdateCommand

BASE_URL: str = "/api/core/groups"


""" Create """


def test_integration_create_group_happy(client: TestClient, group_create_command: GroupCreateCommand):
    body = group_create_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    assert response.status_code == 201
    assert data["code"] == group_create_command.code
    assert data["webname"] == group_create_command.webname
    assert data["active"] is True
    assert data["id"] is not None


def test_integration_create_group_no_code(client: TestClient, group_create_command: GroupCreateCommand):
    group_create_command.code = None
    body = group_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_integration_create_group_no_webname(client: TestClient, group_create_command: GroupCreateCommand):
    group_create_command.webname = None
    body = group_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


""" Update """


def test_integration_update_group_happy(
    client: TestClient, session: Session, group_update_command: GroupUpdateCommand, group_in_db: Group
):
    body = group_update_command.model_dump()
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    data = response.json()
    assert response.status_code == 200
    assert data["code"] == group_update_command.code
    assert data["webname"] == group_update_command.webname
    assert data["active"] == group_in_db.active
    assert data["id"] == group_in_db.id


def test_integration_update_group_no_code(
    client: TestClient, session: Session, group_update_command: GroupUpdateCommand, group_in_db: Group
):
    group_update_command.code = None
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    assert response.status_code == 422


def test_integration_update_group_no_webname(
    client: TestClient, session: Session, group_update_command: GroupUpdateCommand, group_in_db: Group
):
    group_update_command.webname = None
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    assert response.status_code == 422


def test_integration_update_group_no_active(
    client: TestClient, session: Session, group_update_command: GroupUpdateCommand, group_in_db: Group
):
    group_update_command.active = None
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    assert response.status_code == 422
