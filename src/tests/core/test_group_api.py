from fastapi.testclient import TestClient

from src.app.main import app
from src.app.modules.core.domain.group_service import GroupService
from src.app.modules.core.domain.models import GroupCreateCommand
from src.tests.core.conftest import GroupServiceMock


def test_integration_create_group_happy(client: TestClient, group_create_command: GroupCreateCommand):
    body = group_create_command.model_dump()
    response = client.post("/api/core/groups", json=body)
    data = response.json()
    assert response.status_code == 201
    assert data["code"] == group_create_command.code
    assert data["webname"] == group_create_command.webname
    assert data["active"] is True
    assert data["id"] is not None


def test_unit_create_group_happy(client_simple: TestClient, group_create_command: GroupCreateCommand, group_service):
    app.dependency_overrides[GroupService] = GroupServiceMock
    body = group_create_command.model_dump()
    response = client_simple.post("/api/core/groups", json=body)
    app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 201
    assert data["code"] == group_create_command.code
    assert data["webname"] == group_create_command.webname
    assert data["active"] is True
    assert data["id"] is not None
