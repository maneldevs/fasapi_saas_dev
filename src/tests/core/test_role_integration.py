from fastapi.testclient import TestClient
from sqlmodel import Session

from src.app.modules.core.domain.models import Menu, Permission, PermissionCreateCommand, Resource, Role, RoleCommand, RoleMenu, User

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


def test_i_create_happy(client: TestClient, session: Session, role_command: RoleCommand):
    body = role_command.model_dump()
    response = client.post(BASE_URL, json=body)
    data = response.json()
    created = session.get(Role, {data["id"]})
    assert response.status_code == 201
    assert created is not None
    assert data["code"] == role_command.code
    assert data["webname"] == role_command.webname
    assert data["id"] is not None
    assert data["code"] == created.code
    assert data["webname"] == created.webname
    assert data["id"] == created.id


def test_i_create_no_code(client: TestClient, role_command: RoleCommand):
    role_command.code = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


def test_i_create_no_webname(client: TestClient, role_command: RoleCommand):
    role_command.webname = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.post(BASE_URL, json=body)
    assert response.status_code == 422


""" Update """


def test_i_update_happy(client: TestClient, session: Session, role_command: RoleCommand, role_in_db: Role):
    body = role_command.model_dump()
    response = client.put(f"{BASE_URL}/{role_in_db.id}", json=body)
    data = response.json()
    module_updated = session.get(Role, {data["id"]})
    assert module_updated is not None
    assert response.status_code == 200
    assert data["code"] == role_command.code
    assert data["webname"] == role_command.webname
    assert data["id"] == role_in_db.id
    assert data["code"] == module_updated.code
    assert data["webname"] == module_updated.webname
    assert data["id"] == module_updated.id


def test_i_update_no_code(client: TestClient, role_command: RoleCommand, role_in_db: Role):
    role_command.code = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{role_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_webname(client: TestClient, role_command: RoleCommand, role_in_db: Role):
    role_command.webname = None
    body = role_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/{role_in_db.id}", json=body)
    assert response.status_code == 422


def test_i_update_no_existent(client: TestClient, role_command: RoleCommand):
    body = role_command.model_dump(exclude_defaults=True)
    response = client.put(f"{BASE_URL}/8888", json=body)
    assert response.status_code == 404


""" Delete """


def test_i_delete_happy(client: TestClient, session: Session, role_in_db: Role):
    response = client.delete(f"{BASE_URL}/{role_in_db.id}")
    role_in_db_after = session.get(Role, role_in_db.id)
    assert response.status_code == 204
    assert role_in_db_after is None


def test_i_delete_no_existent(client: TestClient):
    response = client.delete(f"{BASE_URL}/8888")
    assert response.status_code == 404


def test_i_delete_role_with_dependants(client: TestClient, user_in_db: User):
    response = client.delete(f"{BASE_URL}/{user_in_db.role.id}")
    assert response.status_code == 400


""" Read resource index """


def test_id_read_permission_index_happy(client: TestClient, permissions_in_db: list[Permission]):
    role = permissions_in_db[0].role
    response = client.get(f"{BASE_URL}/{role.id}/permissions/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2

    assert data[0]["id"] == permissions_in_db[0].id
    assert data[0]["scope"] == permissions_in_db[0].scope
    assert data[0]["scope_owner"] == permissions_in_db[0].scope_owner
    assert data[0]["resource"]["id"] == permissions_in_db[0].resource.id
    assert data[0]["resource"]["code"] == permissions_in_db[0].resource.code
    assert data[0]["resource"]["module"]["id"] == permissions_in_db[0].resource.module.id
    assert data[0]["resource"]["module"]["code"] == permissions_in_db[0].resource.module.code
    assert data[0]["resource"]["module"]["webname"] == permissions_in_db[0].resource.module.webname

    assert data[1]["id"] == permissions_in_db[1].id
    assert data[1]["scope"] == permissions_in_db[1].scope
    assert data[1]["scope_owner"] == permissions_in_db[1].scope_owner
    assert data[1]["resource"]["id"] == permissions_in_db[1].resource.id
    assert data[1]["resource"]["code"] == permissions_in_db[1].resource.code
    assert data[1]["resource"]["module"]["id"] == permissions_in_db[1].resource.module.id
    assert data[1]["resource"]["module"]["code"] == permissions_in_db[1].resource.module.code
    assert data[1]["resource"]["module"]["webname"] == permissions_in_db[1].resource.module.webname


def test_id_read_permission_index_with_module_filter_happy(client: TestClient, permissions_in_db: list[Permission]):
    role = permissions_in_db[0].role
    params = {"module_id": permissions_in_db[0].resource.module_id}
    response = client.get(f"{BASE_URL}/{role.id}/permissions/index", params=params)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2


def test_id_read_permission_index_with_module_filter_no_matches(
    client: TestClient, permissions_in_db: list[Permission]
):
    role = permissions_in_db[0].role
    params = {"module_id": "8888"}
    response = client.get(f"{BASE_URL}/{role.id}/permissions/index", params=params)
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


def test_id_read_permission_index_none_in_db(client: TestClient, role_in_db: Role):
    response = client.get(f"{BASE_URL}/{role_in_db.id}/permissions/index")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


def test_id_read_permission_module_no_exists(client: TestClient):
    response = client.get(f"{BASE_URL}/888/permissions/index")
    assert response.status_code == 404


""" Create permission """


def test_i_create_permission_happy(
    client: TestClient,
    session: Session,
    permission_create_command: PermissionCreateCommand,
    role_in_db: Role,
    resource_in_db: Resource,
):
    body = permission_create_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/{role_in_db.id}/permissions", json=body)
    data = response.json()
    created = session.get(Permission, {data["id"]})
    assert response.status_code == 201
    assert created is not None
    assert data["id"] == created.id
    assert data["scope"] == permission_create_command.scope == created.scope
    assert data["scope_owner"] == permission_create_command.scope_owner == created.scope_owner
    assert data["resource"]["id"] == created.resource.id == permission_create_command.resource_id
    assert data["resource"]["code"] == created.resource.code
    assert data["resource"]["module"]["id"] == created.resource.module.id
    assert data["resource"]["module"]["code"] == created.resource.module.code
    assert data["resource"]["module"]["webname"] == created.resource.module.webname
    assert data["role"]["id"] == created.role.id == role_in_db.id
    assert data["role"]["code"] == created.role.code
    assert data["role"]["webname"] == created.role.webname


def test_i_create_permission_no_scope_happy(
    client: TestClient,
    session: Session,
    permission_create_command: PermissionCreateCommand,
    role_in_db: Role,
    resource_in_db: Resource,
):
    permission_create_command.scope = None
    body = permission_create_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/{role_in_db.id}/permissions", json=body)
    data = response.json()
    created = session.get(Permission, {data["id"]})
    assert response.status_code == 201
    assert created is not None
    assert data["scope"] is None


def test_i_create_permission_no_resource_id(
    client: TestClient, permission_create_command: PermissionCreateCommand, role_in_db: Role
):
    permission_create_command.resource_id = None
    body = permission_create_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/{role_in_db.id}/permissions", json=body)
    assert response.status_code == 422


def test_i_create_permission_role_no_exists(client: TestClient, permission_create_command: PermissionCreateCommand):
    body = permission_create_command.model_dump(exclude_defaults=True)
    response = client.post(f"{BASE_URL}/8888/permissions", json=body)
    assert response.status_code == 404


""" Update role menus """


def test_i_update_menus_happy(client: TestClient, session: Session, role_in_db: Role, menu_child_in_db: Menu):
    body = [menu_child_in_db.id, menu_child_in_db.parent.id]
    response = client.patch(f"{BASE_URL}/{role_in_db.id}/menus", json=body)
    data = response.json()
    updated = session.get(Role, role_in_db.id)
    assert response.status_code == 200
    assert updated.id == role_in_db.id
    assert updated.code == role_in_db.code
    assert updated.webname == role_in_db.webname
    assert len(updated.menus) == 2
    assert menu_child_in_db.id in [menu.id for menu in updated.menus]
    assert menu_child_in_db.parent.id in [menu.id for menu in updated.menus]
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


def test_i_update_menus_role_no_exists(client: TestClient, menu_child_in_db: Menu):
    body = [menu_child_in_db.id, menu_child_in_db.parent.id]
    response = client.patch(f"{BASE_URL}/8888/menus", json=body)
    assert response.status_code == 404


def test_i_update_menus_menu_no_exists(client: TestClient, role_in_db: Role):
    body = ["nonexistent"]
    response = client.patch(f"{BASE_URL}/{role_in_db.id}/menus", json=body)
    assert response.status_code == 404


""" Read role menu tree """


def test_i_read_menu_tree_happy(client: TestClient, session: Session, role_in_db: Role, menu_child_in_db: Menu):
    role_menu_child = RoleMenu(menu_id=menu_child_in_db.id, role_id=role_in_db.id)
    role_menu_parent = RoleMenu(menu_id=menu_child_in_db.parent.id, role_id=role_in_db.id)
    session.add(role_menu_child)
    session.add(role_menu_parent)
    session.commit()
    response = client.get(f"{BASE_URL}/{role_in_db.id}/menus/tree")
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


def test_i_read_menu_no_parents(client: TestClient, session: Session, role_in_db: Role, menu_child_in_db: Menu):
    role_menu_child = RoleMenu(menu_id=menu_child_in_db.id, role_id=role_in_db.id)
    session.add(role_menu_child)
    session.commit()
    response = client.get(f"{BASE_URL}/{role_in_db.id}/menus/tree")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 0


def test_i_read_menu_no_children(client: TestClient, session: Session, role_in_db: Role, menu_parent_in_db: Menu):
    role_menu_parent = RoleMenu(menu_id=menu_parent_in_db.id, role_id=role_in_db.id)
    session.add(role_menu_parent)
    session.commit()
    response = client.get(f"{BASE_URL}/{role_in_db.id}/menus/tree")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == menu_parent_in_db.id
    assert data[0]["code"] == menu_parent_in_db.code
    assert data[0]["link"] == menu_parent_in_db.link
    assert data[0]["module"]["id"] == menu_parent_in_db.module_id
    assert data[0]["module"]["code"] == menu_parent_in_db.module.code
    assert data[0]["module"]["webname"] == menu_parent_in_db.module.webname


def test_i_read_menu_tree_role_no_exists(client: TestClient):
    response = client.get(f"{BASE_URL}/8888/menus/tree")
    assert response.status_code == 404