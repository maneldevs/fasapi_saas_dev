from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import Configuration, ConfigurationCommand, Module

BASE_URL: str = "/api/core/configurations"


""" Read index """


def test_read_index_happy(client: TestClient, configurations_in_db: list[Configuration]):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == configurations_in_db[0].id
    assert data[0]["code"] == configurations_in_db[0].code
    assert data[0]["module"]["id"] == configurations_in_db[0].module.id
    assert data[0]["module"]["code"] == configurations_in_db[0].module.code
    assert data[0]["module"]["webname"] == configurations_in_db[0].module.webname
    assert data[1]["id"] == configurations_in_db[1].id
    assert data[1]["code"] == configurations_in_db[1].code
    assert data[1]["module"]["id"] == configurations_in_db[1].module.id
    assert data[1]["module"]["code"] == configurations_in_db[1].module.code
    assert data[1]["module"]["webname"] == configurations_in_db[1].module.webname


def test_read_index_no_data(client: TestClient):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


""" Read by id """


def test_read_configuration_happy(client: TestClient, configuration_in_db: Configuration):
    response = client.get(f"{BASE_URL}/{configuration_in_db.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == configuration_in_db.id
    assert data["code"] == configuration_in_db.code
    assert data["module"]["id"] == configuration_in_db.module.id
    assert data["module"]["code"] == configuration_in_db.module.code
    assert data["module"]["webname"] == configuration_in_db.module.webname


def test_read_configuration_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Create """


def test_create_configuration_happy(
    client: TestClient, session: Session, configuration_command: ConfigurationCommand, module_in_db: Module
):
    body = configuration_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    configuration_created = session.get(Configuration, {data["id"]})
    assert response.status_code == 201
    assert data["id"] is not None
    assert data["code"] == configuration_command.code == configuration_created.code
    assert data["module"]["id"] == configuration_command.module_id == configuration_created.module.id
    assert data["module"]["code"] == configuration_created.module.code
    assert data["module"]["webname"] == configuration_created.module.webname


def test_create_configuration_no_code(client: TestClient, configuration_command: ConfigurationCommand):
    configuration_command.code = None
    body = configuration_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_create_configuration_nonexistent_module(client: TestClient, configuration_command: ConfigurationCommand):
    configuration_command.module_id = "nonexistent"
    body = configuration_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 404


def test_create_configuration_already_exists(
    client: TestClient,
    session: Session,
    configuration_command: ConfigurationCommand,
    configuration_in_db: Configuration,
):
    configuration_command.code = configuration_in_db.code
    body = configuration_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 400


""" Update """


def test_update_configuration_happy(
    client: TestClient,
    session: Session,
    configuration_command: ConfigurationCommand,
    configuration_in_db: Configuration,
):
    body = configuration_command.model_dump()
    response = client.put(f"{BASE_URL}/{configuration_in_db.id}", json=body)
    data = response.json()
    configuration_updated = session.get(Configuration, {data["id"]})
    assert configuration_updated is not None
    assert response.status_code == 200
    assert data["id"] == configuration_in_db.id
    assert data["code"] == configuration_command.code == configuration_updated.code
    assert data["module"]["id"] == configuration_command.module_id == configuration_updated.module.id
    assert data["module"]["code"] == configuration_updated.module.code
    assert data["module"]["webname"] == configuration_updated.module.webname


def test_update_configuration_no_code(
    client: TestClient, configuration_command: ConfigurationCommand, configuration_in_db: Configuration
):
    configuration_command.code = None
    body = configuration_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{configuration_in_db.id}", json=body)
    assert response.status_code == 422


def test_update_configuration_nonexistent_module(
    client: TestClient, configuration_command: ConfigurationCommand, configuration_in_db: Configuration
):
    configuration_command.module_id = "nonexistent"
    body = configuration_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{configuration_in_db.id}", json=body)
    assert response.status_code == 404


def test_update_configuration_already_exists(
    client: TestClient,
    configuration_command: ConfigurationCommand,
    configurations_in_db: list[Configuration],
):
    configuration_command.code = configurations_in_db[1].code
    body = configuration_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{configurations_in_db[0].id}", json=body)
    assert response.status_code == 400


def test_update_configuration_no_existent(client: TestClient, configuration_command: ConfigurationCommand):
    body = configuration_command.model_dump()
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_delete_configuration_happy(client: TestClient, session: Session, configuration_in_db: Configuration):
    response = client.delete(f"{BASE_URL}/{configuration_in_db.id}")
    configuration_in_db_after = session.get(Configuration, configuration_in_db.id)
    assert response.status_code == 204
    assert configuration_in_db_after is None


def test_delete_configuration_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404
