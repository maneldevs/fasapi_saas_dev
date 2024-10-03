import pytest
from sqlmodel import Session

from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.models import (
    Configuration,
    ConfigurationCommand,
    ConfigurationValue,
    ConfigurationValueCommand,
    Group,
    GroupCreateCommand,
    GroupUpdateCommand,
    Menu,
    MenuCommand,
    Module,
    ModuleCommand,
    Permission,
    PermissionCreateCommand,
    PermissionUpdateCommand,
    Resource,
    ResourceCreateCommand,
    ResourceUpdateCommand,
    Role,
    RoleCommand,
    User,
    UserCreateCommand,
    UserUpdateCommand,
)
from src.app.main import app


""" Group """


class GroupServiceMock:
    def create(self, command: GroupCreateCommand) -> Group:
        return Group(id="abc-123-def-456", code=command.code, webname=command.webname, active=True)


@pytest.fixture(name="group_create_command")
def group_create_command_fixture():
    return GroupCreateCommand(code="ABC-123", webname="ABC")


@pytest.fixture(name="group_update_command")
def group_update_command_fixture():
    return GroupUpdateCommand(code="DEF-456", webname="DEF", active=False)


@pytest.fixture(name="group")
def group_fixture():
    return Group(id="abc-123-def-456", code="ABC-123", webname="ABC", active=True)


@pytest.fixture(name="group2")
def group2_fixture():
    return Group(id="ghi-123-jkl-456", code="GHI-123", webname="GHI", active=False)


@pytest.fixture(name="group_in_db")
def group_in_db_fixture(session: Session, group: Group):
    session.add(group)
    session.commit()
    return group


@pytest.fixture(name="groups_in_db")
def groups_in_db_fixture(session: Session, group: Group, group2: Group):
    session.add(group)
    session.add(group2)
    session.commit()
    return [group, group2]


@pytest.fixture(name="group_service")
def group_service_fixture():
    app.dependency_overrides[GroupService] = GroupServiceMock
    yield
    app.dependency_overrides.clear()


""" Role """


@pytest.fixture(name="role_command")
def role_command_fixture():
    return RoleCommand(code="ROLE1", webname="role1 ")


@pytest.fixture(name="role")
def role_fixture():
    return Role(id="abc-123-def-456", code="ROLE1", webname="role 1")


@pytest.fixture(name="role2")
def role2_fixture():
    return Role(id="ghi-123-jkl-456", code="ROLE2", webname="role 2")


@pytest.fixture(name="role_in_db")
def role_in_db_fixture(session: Session, role: Role):
    session.add(role)
    session.commit()
    return role


@pytest.fixture(name="roles_in_db")
def roles_in_db_fixture(session: Session, role: Role, role2: Role):
    session.add(role)
    session.add(role2)
    session.commit()
    return [role, role2]


""" User """


@pytest.fixture(name="user_create_command")
def user_create_command_fixture(role_in_db: Role, group_in_db: Group):
    return UserCreateCommand(
        username="Myusername",
        password_raw="secret",
        firstname="Myfirstname",
        lastname="MyLastname",
        group_id=group_in_db.id,
        role_id=role_in_db.id,
    )


@pytest.fixture(name="user_update_command")
def user_update_command_fixture(roles_in_db: Role, groups_in_db: Group):
    return UserUpdateCommand(
        username="MyusernameChanged",
        password_raw="secretChanged",
        firstname="MyfirstnameChanged",
        lastname="MyLastnameChanged",
        active=False,
        is_god=True,
        group_id=groups_in_db[1].id,
        role_id=roles_in_db[1].id,
    )


@pytest.fixture(name="user")
def user_fixture():
    return User(
        id="abc-123-def-456",
        username="Myusername",
        password="secret_encoded",
        firstname="Myfirstname",
        lastname="MyLastname",
        group_id="abc-123-def-456",
        role_id="abc-123-def-456",
    )


@pytest.fixture(name="user2")
def user2_fixture():
    return User(
        id="ghi-123-jkl-456",
        username="Otherusername",
        password="secret_encoded",
        firstname="Otherfirstname",
        lastname="OtherLastname",
        group_id="abc-123-def-456",
        role_id="abc-123-def-456",
    )


@pytest.fixture(name="user_in_db")
def user_in_db_fixture(session: Session, user: User, role_in_db: Role, group_in_db: Group):
    user.role_id = role_in_db.id
    user.group_id = group_in_db.id
    session.add(user)
    session.commit()
    return user


@pytest.fixture(name="users_in_db")
def users_in_db_fixture(session: Session, user: User, user2: User, role_in_db: Role, group_in_db: Group):
    user.role_id = role_in_db.id
    user.group_id = group_in_db.id
    user2.role_id = role_in_db.id
    user2.group_id = group_in_db.id
    session.add(user)
    session.add(user2)
    session.commit()
    return [user, user2]


""" Module """


@pytest.fixture(name="module_command")
def module_command_fixture():
    return ModuleCommand(code="MODULE1", webname="module 1")


@pytest.fixture(name="module")
def module_fixture():
    return Module(id="abc-123-def-456", code="MODULE1", webname="module 1")


@pytest.fixture(name="module2")
def module2_fixture():
    return Module(id="ghi-123-jkl-456", code="MODULE2", webname="module 2")


@pytest.fixture(name="module_in_db")
def module_in_db_fixture(session: Session, module: Module):
    session.add(module)
    session.commit()
    return module


@pytest.fixture(name="modules_in_db")
def modules_in_db_fixture(session: Session, module: Module, module2: Module):
    session.add(module)
    session.add(module2)
    session.commit()
    return [module, module2]


""" Module Resource """


@pytest.fixture(name="resource_create_command")
def resource_create_command_fixture():
    return ResourceCreateCommand(code="RESOURCE_CHANGED")


@pytest.fixture(name="resource_update_command")
def resource_update_command_fixture():
    return ResourceUpdateCommand(code="RESOURCE_CHANGED", module_id="abc-123-def-456")


@pytest.fixture(name="resource")
def resource_fixture(module: Module):
    return Resource(id="abc-123-def-456", code="RESOURCE1", module_id=module.id, module=module)


@pytest.fixture(name="resource2")
def resource2_fixture(module: Module):
    return Resource(id="ghi-123-jkl-456", code="RESOURCE2", module_id=module.id, module=module)


@pytest.fixture(name="resource_in_db")
def resource_in_db_fixture(session: Session, resource: Resource, module_in_db: Module):
    resource.module_id = module_in_db.id
    session.add(resource)
    session.commit()
    return resource


@pytest.fixture(name="resources_in_db")
def resources_in_db_fixture(session: Session, resource: Resource, resource2: Resource, module_in_db: Module):
    resource.module_id = module_in_db.id
    resource2.module_id = module_in_db.id
    session.add(resource)
    session.add(resource2)
    session.commit()
    return [resource, resource2]


""" Permission """


@pytest.fixture(name="permission_create_command")
def permission_create_command_fixture():
    return PermissionCreateCommand(scope="CRUD", scope_owner="R", resource_id="abc-123-def-456")


@pytest.fixture(name="permission_update_command")
def permission_update_command_fixture():
    return PermissionUpdateCommand(scope="R", scope_owner="CRUD")


@pytest.fixture(name="permission")
def permission_fixture(role: Role, resource: Resource):
    return Permission(
        id="abc-123-def-456",
        scope="R",
        scope_owner="CRUD",
        role_id=role.id,
        role=role,
        resource_id=resource.id,
        resource=resource,
    )


@pytest.fixture(name="permission2")
def permission2_fixture(role: Role, resource2: Resource):
    return Permission(
        id="ghi-123-jkl-456",
        scope="CRUD",
        scope_owner="R",
        role_id=role.id,
        role=role,
        resource_id=resource2.id,
        resource=resource2,
    )


@pytest.fixture(name="permission_in_db")
def permission_in_db_fixture(session: Session, permission: Permission, role_in_db: Role, resource_in_db: Resource):
    permission.role_id = role_in_db.id
    permission.resource_id = resource_in_db.id
    session.add(permission)
    session.commit()
    return permission


@pytest.fixture(name="permissions_in_db")
def permissions_in_db_fixture(
    session: Session, permission: Permission, permission2: Permission, role_in_db: Role, resources_in_db: list[Resource]
):
    permission.role_id = role_in_db.id
    permission.resource_id = resources_in_db[0].id
    permission2.role_id = role_in_db.id
    permission2.resource_id = resources_in_db[1].id
    session.add(permission)
    session.add(permission2)
    session.commit()
    return [permission, permission2]


""" Menu """


@pytest.fixture(name="menu_parent_command")
def menu_parent_command_fixture():
    return MenuCommand(code="menu 1", link="link 1", module_id="abc-123-def-456")


@pytest.fixture(name="menu_child_command")
def menu_child_command_fixture():
    return MenuCommand(code="menu 11", link="link 11", module_id="abc-123-def-456", parent_id="abc-123-def-456")


@pytest.fixture(name="menu_parent")
def menu_parent_fixture(module: Module):
    return Menu(id="abc-123-def-456", code="menu 1", link="link 1", module_id=module.id, module=module)


@pytest.fixture(name="menu_child")
def menu_child_fixture(menu_parent: Menu, module: Module):
    return Menu(
        id="ghi-123-jkl-456",
        code="menu 11",
        link="link 11",
        module_id=module.id,
        module=module,
        parent_id=menu_parent.id,
        parent=menu_parent,
    )


@pytest.fixture(name="menu_parent_in_db")
def menu_parent_in_db_fixture(session: Session, menu_parent: Menu, module_in_db: Module):
    menu_parent.module_id = module_in_db.id
    session.add(menu_parent)
    session.commit()
    return menu_parent


@pytest.fixture(name="menu_child_in_db")
def menu_child_in_db_fixture(session: Session, menu_parent_in_db: Menu, menu_child: Menu, module_in_db: Module):
    menu_child.module_id = module_in_db.id
    menu_child.parent_id = menu_parent_in_db.id
    session.add(menu_child)
    session.commit()
    return menu_child


""" Configuration """


@pytest.fixture(name="configuration_command")
def configuration_command_fixture():
    return ConfigurationCommand(code="CONFIG1", module_id="abc-123-def-456")


@pytest.fixture(name="configuration")
def configuration_fixture(module: Module):
    return Configuration(id="abc-123-def-456", code="CONFIG1", module=module, module_id=module.id)


@pytest.fixture(name="configuration2")
def configuration2_fixture(module: Module):
    return Configuration(id="ghi-123-jkl-456", code="CONFIG2", module=module, module_id=module.id)


@pytest.fixture(name="configuration_in_db")
def configuration_in_db_fixture(session: Session, configuration: Configuration, module_in_db: Module):
    configuration.module_id = module_in_db.id
    session.add(configuration)
    session.commit()
    return configuration


@pytest.fixture(name="configurations_in_db")
def configurations_in_db_fixture(
    session: Session, configuration: Configuration, configuration2: Configuration, module_in_db: Module
):
    configuration.module_id = module_in_db.id
    configuration2.module_id = module_in_db.id
    session.add(configuration)
    session.add(configuration2)
    session.commit()
    return [configuration, configuration2]


""" Configuration Value """


@pytest.fixture(name="configuration_value_command")
def configuration_value_command_fixture(configuration_in_db: Configuration):
    return ConfigurationValueCommand(configuration_id=configuration_in_db.id, value="value1")


@pytest.fixture(name="configuration_value")
def configuration_value_fixture(configuration: Configuration, group: Group):
    return ConfigurationValue(
        id="abc-123-def-456",
        configuration_id=configuration.id,
        configuration=configuration,
        group_id=group.id,
        group=group,
        value="value1",
    )


@pytest.fixture(name="configuration_value2")
def configuration_value2_fixture(configuration2: Configuration, group: Group):
    return ConfigurationValue(
        id="ghi-123-jkl-456",
        configuration_id=configuration2.id,
        configuration=configuration2,
        group_id=group.id,
        group=group,
        value="value2",
    )


@pytest.fixture(name="configuration_value_in_db")
def configuration_value_in_db_fixture(
    session: Session, configuration_value: ConfigurationValue, configuration_in_db: Configuration, group_in_db: Group
):
    configuration_value.configuration_id = configuration_in_db.id
    configuration_value.group_id = group_in_db.id
    session.add(configuration_value)
    session.commit()
    return configuration_value


@pytest.fixture(name="configuration_values_in_db")
def configuration_values_in_db_fixture(
    session: Session,
    configuration_value: ConfigurationValue,
    configuration_value2: ConfigurationValue,
    configurations_in_db: list[Configuration],
    group_in_db: Group,
):
    configuration_value.configuration_id = configurations_in_db[0].id
    configuration_value.group_id = group_in_db.id
    configuration_value2.configuration_id = configurations_in_db[1].id
    configuration_value2.group_id = group_in_db.id
    session.add(configuration_value)
    session.add(configuration_value2)
    session.commit()
    return [configuration_value, configuration_value2]
