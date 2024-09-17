from fastapi.testclient import TestClient
from pytest import Module
from sqlmodel import Session

from src.app.modules.core.domain.models import Menu, MenuCommand

BASE_URL: str = "/api/core/menus"


""" Read tree """


def test_id_read_index_happy(client: TestClient, menu_child_in_db: list[Menu]):
    response = client.get(f"{BASE_URL}/tree")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == menu_child_in_db.parent.id
    assert data[0]["code"] == menu_child_in_db.parent.code
    assert data[0]["link"] == menu_child_in_db.parent.link
    assert data[0]["module"]["id"] == menu_child_in_db.parent.module_id
    assert data[0]["module"]["code"] == menu_child_in_db.parent.module.code
    assert data[0]["module"]["webname"] == menu_child_in_db.parent.module.webname
    assert data[0]["children"][0]["id"] == menu_child_in_db.id
    assert data[0]["children"][0]["code"] == menu_child_in_db.code
    assert data[0]["children"][0]["link"] == menu_child_in_db.link
    assert data[0]["children"][0]["module"]["id"] == menu_child_in_db.module_id
    assert data[0]["children"][0]["module"]["code"] == menu_child_in_db.module.code
    assert data[0]["children"][0]["module"]["webname"] == menu_child_in_db.module.webname


def test_id_read_index_none_in_db(client: TestClient):
    response = client.get(f"{BASE_URL}/tree")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


""" Read by id """


def test_id_read_by_id_parent_happy(client: TestClient, menu_parent_in_db: Menu):
    response = client.get(f"{BASE_URL}/{menu_parent_in_db.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == menu_parent_in_db.id
    assert data["code"] == menu_parent_in_db.code
    assert data["link"] == menu_parent_in_db.link
    assert data["parent"] is None
    assert data["module"]["id"] == menu_parent_in_db.module_id
    assert data["module"]["code"] == menu_parent_in_db.module.code
    assert data["module"]["webname"] == menu_parent_in_db.module.webname


def test_id_read_by_id_child_happy(client: TestClient, menu_child_in_db: Menu):
    response = client.get(f"{BASE_URL}/{menu_child_in_db.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == menu_child_in_db.id
    assert data["code"] == menu_child_in_db.code
    assert data["link"] == menu_child_in_db.link
    assert data["module"]["id"] == menu_child_in_db.module_id
    assert data["module"]["code"] == menu_child_in_db.module.code
    assert data["module"]["webname"] == menu_child_in_db.module.webname
    assert data["parent"]["id"] == menu_child_in_db.parent_id
    assert data["parent"]["code"] == menu_child_in_db.parent.code
    assert data["parent"]["link"] == menu_child_in_db.parent.link
    assert data["parent"]["module"]["id"] == menu_child_in_db.parent.module_id
    assert data["parent"]["module"]["code"] == menu_child_in_db.parent.module.code
    assert data["parent"]["module"]["webname"] == menu_child_in_db.parent.module.webname


def test_id_read_by_id_no_existent(client: TestClient):
    response = client.get(f"{BASE_URL}/8888")
    assert response.status_code == 404


""" Create """


def test_i_create_menu_parent_happy(
    client: TestClient, session: Session, menu_parent_command: MenuCommand, module_in_db: Module
):
    body = menu_parent_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    created = session.get(Menu, data["id"])

    assert response.status_code == 201
    assert created is not None

    assert data["id"] == created.id
    assert data["code"] == menu_parent_command.code == created.code
    assert data["link"] == menu_parent_command.link == created.link
    assert data["parent"] is None
    assert data["module"]["id"] == menu_parent_command.module_id == module_in_db.id
    assert data["module"]["code"] == module_in_db.code
    assert data["module"]["webname"] == module_in_db.webname


def test_i_create_menu_child_happy(
    client: TestClient, session: Session, menu_child_command: MenuCommand, module_in_db: Module, menu_parent_in_db
):
    body = menu_child_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    created = session.get(Menu, data["id"])
    assert response.status_code == 201
    assert created is not None
    assert data["id"] == created.id
    assert data["code"] == menu_child_command.code == created.code
    assert data["link"] == menu_child_command.link == created.link
    assert data["module"]["id"] == menu_child_command.module_id == module_in_db.id
    assert data["module"]["code"] == module_in_db.code
    assert data["module"]["webname"] == module_in_db.webname
    assert data["parent"]["id"] == menu_child_command.parent_id == menu_parent_in_db.id
    assert data["parent"]["code"] == menu_parent_in_db.code
    assert data["parent"]["link"] == menu_parent_in_db.link
    assert data["parent"]["module"]["id"] == menu_child_command.module_id == module_in_db.id
    assert data["parent"]["module"]["code"] == module_in_db.code
    assert data["parent"]["module"]["webname"] == module_in_db.webname


def test_i_create_menu_no_code(client: TestClient, menu_parent_command: MenuCommand):
    pass
    menu_parent_command.code = None
    body = menu_parent_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_menu_no_module_id(client: TestClient, menu_parent_command: MenuCommand):
    menu_parent_command.module_id = None
    body = menu_parent_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_menu_with_non_existent_module(client: TestClient, menu_parent_command: MenuCommand):
    menu_parent_command.module_id = "nonexistent"
    body = menu_parent_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 404


def test_i_create_menu_with_non_existent_parent(client: TestClient, menu_child_command: MenuCommand):
    menu_child_command.parent_id = "nonexistent"
    body = menu_child_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 404


def test_i_create_menu_already_existent(client: TestClient, menu_parent_command: MenuCommand, menu_parent_in_db: Menu):
    menu_parent_command.code = menu_parent_in_db.code
    body = menu_parent_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 400


""" Update """


def test_i_update_happy(client: TestClient, session: Session, menu_child_command: MenuCommand, menu_child_in_db: Menu):
    body = menu_child_command.model_dump()
    response = client.put(f"{BASE_URL}/{menu_child_in_db.id}", json=body)
    data = response.json()
    menu_updated = session.get(Menu, {data["id"]})
    assert menu_updated is not None
    assert response.status_code == 200
    assert data["id"] == menu_child_in_db.id == menu_updated.id
    assert data["code"] == menu_child_command.code == menu_updated.code
    assert data["link"] == menu_child_command.link == menu_updated.link
    assert data["module"]["id"] == menu_child_command.module_id == menu_updated.module.id
    assert data["module"]["code"] == menu_updated.module.code
    assert data["module"]["webname"] == menu_updated.module.webname
    assert data["parent"]["id"] == menu_child_command.parent_id == menu_updated.parent.id
    assert data["parent"]["code"] == menu_updated.parent.code
    assert data["parent"]["link"] == menu_updated.parent.link
    assert data["parent"]["module"]["id"] == menu_updated.parent.module.id
    assert data["parent"]["module"]["code"] == menu_updated.parent.module.code
    assert data["parent"]["module"]["webname"] == menu_updated.parent.module.webname


def test_i_update_no_code(client: TestClient, menu_child_command: MenuCommand, menu_child_in_db: Menu):
    menu_child_command.code = None
    body = menu_child_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{menu_child_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_module_id(client: TestClient, menu_child_command: MenuCommand, menu_child_in_db: Menu):
    menu_child_command.module_id = None
    body = menu_child_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{menu_child_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_module_non_existent(client: TestClient, menu_child_command: MenuCommand, menu_child_in_db: Menu):
    menu_child_command.module_id = "nonexistent"
    body = menu_child_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{menu_child_in_db.id}", json=body)
    assert response.status_code == 404


def test_i_update_parent_non_existent(client: TestClient, menu_child_command: MenuCommand, menu_child_in_db: Menu):
    menu_child_command.parent_id = "nonexistent"
    body = menu_child_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{menu_child_in_db.id}", json=body)
    assert response.status_code == 404


def test_i_update_no_existent(client: TestClient, menu_child_command: MenuCommand):
    body = menu_child_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_happy(client: TestClient, session: Session, menu_child_in_db: Menu):
    response = client.delete(f"{BASE_URL}/{menu_child_in_db.id}")
    menu_in_db_after = session.get(Menu, menu_child_in_db.id)
    assert response.status_code == 204
    assert menu_in_db_after is None


def test_i_delete_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404


def test_i_delete_module_with_dependants_cascade(client: TestClient, session: Session, menu_child_in_db: Menu):
    menu_parent_id = menu_child_in_db.parent.id
    menu_child_id = menu_child_in_db.id
    response = client.delete(f"{BASE_URL}/{menu_parent_id}")
    menu_parent = session.get(Menu, menu_parent_id)
    menu_child = session.get(Menu, menu_child_id)
    assert response.status_code == 204
    assert menu_parent is None
    assert menu_child is None
