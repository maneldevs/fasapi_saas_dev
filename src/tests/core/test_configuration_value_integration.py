from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import ConfigurationValue, ConfigurationValueUpdateCommand


BASE_URL: str = "/api/core/configuration-values"

""" Read by id """


def test_i_read_by_id_happy(client: TestClient, configuration_value_in_db: ConfigurationValue):
    response = client.get(f"{BASE_URL}/{configuration_value_in_db.id}")
    data = response.json()
    assert data["id"] == configuration_value_in_db.id
    assert data["value"] == configuration_value_in_db.value
    assert data["configuration"]["id"] == configuration_value_in_db.configuration.id
    assert data["configuration"]["code"] == configuration_value_in_db.configuration.code
    assert data["configuration"]["module"]["id"] == configuration_value_in_db.configuration.module.id
    assert data["configuration"]["module"]["code"] == configuration_value_in_db.configuration.module.code
    assert data["configuration"]["module"]["webname"] == configuration_value_in_db.configuration.module.webname
    assert data["group"]["id"] == configuration_value_in_db.group.id
    assert data["group"]["code"] == configuration_value_in_db.group.code
    assert data["group"]["webname"] == configuration_value_in_db.group.webname


def test_i_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Update """


def test_i_update_happy(
    client: TestClient,
    session: Session,
    configuration_value_update_command: ConfigurationValueUpdateCommand,
    configuration_value_in_db: ConfigurationValue,
):
    body = configuration_value_update_command.model_dump()
    response = client.put(f"{BASE_URL}/{configuration_value_in_db.id}", json=body)
    data = response.json()
    configuration_value_updated = session.get(ConfigurationValue, {data["id"]})
    assert configuration_value_updated is not None
    assert response.status_code == 200
    assert data["id"] == configuration_value_in_db.id
    assert data["value"] == configuration_value_update_command.value == configuration_value_in_db.value
    assert data["configuration"]["id"] == configuration_value_in_db.configuration.id
    assert data["configuration"]["code"] == configuration_value_in_db.configuration.code
    assert data["configuration"]["module"]["id"] == configuration_value_in_db.configuration.module.id
    assert data["configuration"]["module"]["code"] == configuration_value_in_db.configuration.module.code
    assert data["configuration"]["module"]["webname"] == configuration_value_in_db.configuration.module.webname
    assert data["group"]["id"] == configuration_value_in_db.group.id
    assert data["group"]["code"] == configuration_value_in_db.group.code
    assert data["group"]["webname"] == configuration_value_in_db.group.webname


def test_i_update_no_value(
    client: TestClient,
    configuration_value_update_command: ConfigurationValueUpdateCommand,
    configuration_value_in_db: ConfigurationValue,
):
    configuration_value_update_command.value = None
    body = configuration_value_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{configuration_value_in_db.id}", json=body)
    assert response.status_code == 422


""" Delete """


def test_i_delete_happy(client: TestClient, session: Session, configuration_value_in_db: ConfigurationValue):
    response = client.delete(f"{BASE_URL}/{configuration_value_in_db.id}")
    configuration_value_deleted = session.get(ConfigurationValue, {configuration_value_in_db.id})
    assert response.status_code == 204
    assert configuration_value_deleted is None


def test_i_delete_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404
