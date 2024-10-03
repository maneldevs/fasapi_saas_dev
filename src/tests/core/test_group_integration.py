from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import (
    Configuration,
    ConfigurationValue,
    ConfigurationValueCommand,
    Group,
    GroupCreateCommand,
    GroupUpdateCommand,
    Module,
    User,
)

BASE_URL: str = "/api/core/groups"


""" Read """


def test_id_read_paginated_happy(client: TestClient, groups_in_db: list[Group]):
    params = {"page": 2, "size": 1, "order_field": "code", "direction": "desc"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert data["page"] == 2
    assert data["size"] == 1
    assert data["total"] == 2
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == groups_in_db[0].id
    assert data["content"][0]["code"] == groups_in_db[0].code
    assert data["content"][0]["webname"] == groups_in_db[0].webname
    assert data["content"][0]["active"] == groups_in_db[0].active


def test_id_read_filtered_happy(client: TestClient, groups_in_db: list[Group]):
    params = {"target": "abc"}
    response = client.get(f"{BASE_URL}", params=params)
    data = response.json()
    assert len(data["content"]) == 1
    assert data["content"][0]["id"] == groups_in_db[0].id
    assert data["content"][0]["code"] == groups_in_db[0].code
    assert data["content"][0]["webname"] == groups_in_db[0].webname
    assert data["content"][0]["active"] == groups_in_db[0].active


def test_id_read_none_no_params(client: TestClient, groups_in_db: list[Group]):
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


def test_id_read_index_happy(client: TestClient, groups_in_db: list[Group]):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["code"] == groups_in_db[0].code
    assert data[0]["webname"] == groups_in_db[0].webname
    assert data[0]["id"] == groups_in_db[0].id
    assert data[1]["code"] == groups_in_db[1].code
    assert data[1]["webname"] == groups_in_db[1].webname
    assert data[1]["id"] == groups_in_db[1].id


def test_id_read_index_none_in_db(client: TestClient):
    response = client.get(f"{BASE_URL}/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


""" Read by id """


def test_id_read_by_id_happy(client: TestClient, group_in_db: Group):
    response = client.get(f"{BASE_URL}/{group_in_db.id}")
    data = response.json()
    assert data["code"] == group_in_db.code
    assert data["webname"] == group_in_db.webname
    assert data["active"] == group_in_db.active
    assert data["id"] == group_in_db.id


def test_id_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Create """


def test_i_create_group_happy(client: TestClient, session: Session, group_create_command: GroupCreateCommand):
    body = group_create_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    group_created = session.get(Group, {data["id"]})
    assert response.status_code == 201
    assert group_created is not None
    assert data["code"] == group_create_command.code
    assert data["webname"] == group_create_command.webname
    assert data["active"] is True
    assert data["id"] is not None
    assert data["code"] == group_created.code
    assert data["webname"] == group_created.webname
    assert data["active"] == group_created.active
    assert data["id"] == group_created.id


def test_i_create_group_no_code(client: TestClient, group_create_command: GroupCreateCommand):
    group_create_command.code = None
    body = group_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_group_no_webname(client: TestClient, group_create_command: GroupCreateCommand):
    group_create_command.webname = None
    body = group_create_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


""" Update """


def test_i_update_group_happy(
    client: TestClient, session: Session, group_update_command: GroupUpdateCommand, group_in_db: Group
):
    body = group_update_command.model_dump()
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    data = response.json()
    group_updated = session.get(Group, {data["id"]})
    assert group_updated is not None
    assert response.status_code == 200
    assert data["code"] == group_update_command.code
    assert data["webname"] == group_update_command.webname
    assert data["active"] == group_in_db.active
    assert data["id"] == group_in_db.id
    assert data["code"] == group_updated.code
    assert data["webname"] == group_updated.webname
    assert data["active"] == group_updated.active
    assert data["id"] == group_updated.id


def test_i_update_group_no_code(client: TestClient, group_update_command: GroupUpdateCommand, group_in_db: Group):
    group_update_command.code = None
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_group_no_webname(client: TestClient, group_update_command: GroupUpdateCommand, group_in_db: Group):
    group_update_command.webname = None
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_group_no_active(client: TestClient, group_update_command: GroupUpdateCommand, group_in_db: Group):
    group_update_command.active = None
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{group_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_group_no_existent(client: TestClient, group_update_command: GroupUpdateCommand):
    body = group_update_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_group_happy(client: TestClient, session: Session, group_in_db: Group):
    response = client.delete(f"{BASE_URL}/{group_in_db.id}")
    group_in_db_after = session.get(Group, group_in_db.id)
    assert response.status_code == 204
    assert group_in_db_after is None


def test_i_delete_group_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404


def test_i_delete_group_with_dependants(client: TestClient, user_in_db: User):
    response = client.delete(f"{BASE_URL}/{user_in_db.group.id}")
    assert response.status_code == 400


""" Update modules """


def test_i_update_group_modules_happy(
    client: TestClient, session: Session, group_in_db: Group, modules_in_db: list[Module]
):
    body = [module.id for module in modules_in_db]
    response = client.patch(f"{BASE_URL}/{group_in_db.id}/modules", json=body)
    data = response.json()
    group_updated = session.get(Group, group_in_db.id)
    assert group_updated is not None
    assert response.status_code == 200
    assert data["code"] == group_in_db.code
    assert data["webname"] == group_in_db.webname
    assert data["active"] == group_in_db.active
    assert data["id"] == group_in_db.id
    assert data["code"] == group_updated.code
    assert data["webname"] == group_updated.webname
    assert data["active"] == group_updated.active
    assert data["id"] == group_updated.id
    assert len(group_updated.modules) == 2
    assert data["modules"][0]["code"] == modules_in_db[0].code == group_updated.modules[0].code
    assert data["modules"][0]["webname"] == modules_in_db[0].webname == group_updated.modules[0].webname
    assert data["modules"][0]["id"] == modules_in_db[0].id == group_updated.modules[0].id
    assert data["modules"][1]["code"] == modules_in_db[1].code == group_updated.modules[1].code
    assert data["modules"][1]["webname"] == modules_in_db[1].webname == group_updated.modules[1].webname
    assert data["modules"][1]["id"] == modules_in_db[1].id == group_updated.modules[1].id


def test_i_update_group_modules_group_non_existent(client: TestClient, modules_in_db: list[Module]):
    body = [module.id for module in modules_in_db]
    response = client.patch(f"{BASE_URL}/8888/modules", json=body)
    assert response.status_code == 404


def test_i_update_group_modules_with_modules_non_existent(client: TestClient, group_in_db: Group):
    body = ["abc, def"]
    response = client.patch(f"{BASE_URL}/{group_in_db.id}/modules", json=body)
    assert response.status_code == 404


""" Create configuration value """


def test_i_create_configuration_value_happy(
    client: TestClient,
    session: Session,
    group_in_db: Group,
    configuration_in_db: Configuration,
    configuration_value_command: ConfigurationValueCommand,
):
    body = configuration_value_command.model_dump()
    response = client.post(f"{BASE_URL}/{group_in_db.id}/configuration-values", json=body)
    data = response.json()
    configuration_value_created = session.get(ConfigurationValue, data["id"])
    assert response.status_code == 201
    assert configuration_value_created is not None
    assert data["id"] == configuration_value_created.id
    assert data["value"] == configuration_value_command.value == configuration_value_created.value
    assert (
        data["configuration"]["id"]
        == configuration_value_command.configuration_id
        == configuration_value_created.configuration.id
    )
    assert data["configuration"]["code"] == configuration_in_db.code == configuration_value_created.configuration.code
    assert (
        data["configuration"]["module"]["id"]
        == configuration_in_db.module.id
        == configuration_value_created.configuration.module.id
    )
    assert (
        data["configuration"]["module"]["code"]
        == configuration_in_db.module.code
        == configuration_value_created.configuration.module.code
    )
    assert (
        data["configuration"]["module"]["webname"]
        == configuration_in_db.module.webname
        == configuration_value_created.configuration.module.webname
    )
    assert data["group"]["id"] == group_in_db.id == configuration_value_created.group.id
    assert data["group"]["code"] == group_in_db.code == configuration_value_created.group.code
    assert data["group"]["webname"] == group_in_db.webname == configuration_value_created.group.webname


def test_i_create_configuration_value_no_value(
    client: TestClient, group_in_db: Group, configuration_value_command: ConfigurationValueCommand
):
    configuration_value_command.value = None
    body = configuration_value_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/{group_in_db.id}/configuration-values", json=body)
    assert response.status_code == 422


def test_i_create_configuration_value_no_configuration_id(
    client: TestClient, group_in_db: Group, configuration_value_command: ConfigurationValueCommand
):
    configuration_value_command.configuration_id = None
    body = configuration_value_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/{group_in_db.id}/configuration-values", json=body)
    assert response.status_code == 422


def test_i_create_configuration_value_no_existent_configuration_id(
    client: TestClient, group_in_db: Group, configuration_value_command: ConfigurationValueCommand
):
    configuration_value_command.configuration_id = "8888"
    body = configuration_value_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/{group_in_db.id}/configuration-values", json=body)
    assert response.status_code == 404


def test_i_create_configuration_value_no_existent_group_id(
    client: TestClient, configuration_in_db: Configuration, configuration_value_command: ConfigurationValueCommand
):
    body = configuration_value_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/8888/configuration-values", json=body)
    assert response.status_code == 404


""" Read configuration values index """


def test_i_read_configuration_values_index_happy(
    client: TestClient, group_in_db: Group, configuration_values_in_db: list[ConfigurationValue]
):
    response = client.get(f"{BASE_URL}/{group_in_db.id}/configuration-values/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["id"] == configuration_values_in_db[0].id
    assert data[0]["value"] == configuration_values_in_db[0].value
    assert data[0]["configuration"]["id"] == configuration_values_in_db[0].configuration.id
    assert data[0]["configuration"]["code"] == configuration_values_in_db[0].configuration.code
    assert data[0]["configuration"]["module"]["id"] == configuration_values_in_db[0].configuration.module.id
    assert data[0]["configuration"]["module"]["code"] == configuration_values_in_db[0].configuration.module.code
    assert data[0]["configuration"]["module"]["webname"] == configuration_values_in_db[0].configuration.module.webname
    assert data[0]["group"]["id"] == group_in_db.id
    assert data[0]["group"]["code"] == group_in_db.code
    assert data[0]["group"]["webname"] == group_in_db.webname
    assert data[1]["id"] == configuration_values_in_db[1].id
    assert data[1]["value"] == configuration_values_in_db[1].value
    assert data[1]["configuration"]["id"] == configuration_values_in_db[1].configuration.id
    assert data[1]["configuration"]["code"] == configuration_values_in_db[1].configuration.code
    assert data[1]["configuration"]["module"]["id"] == configuration_values_in_db[1].configuration.module.id
    assert data[1]["configuration"]["module"]["code"] == configuration_values_in_db[1].configuration.module.code
    assert data[1]["configuration"]["module"]["webname"] == configuration_values_in_db[1].configuration.module.webname
    assert data[1]["group"]["id"] == group_in_db.id
    assert data[1]["group"]["code"] == group_in_db.code
    assert data[1]["group"]["webname"] == group_in_db.webname


def test_i_read_configuration_values_index_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888/configuration-values/index")
    assert response.status_code == 404
