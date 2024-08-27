import pytest
from sqlmodel import Session

from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.models import (
    Group,
    GroupCreateCommand,
    GroupUpdateCommand,
    Module,
    ModuleCommand,
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
        role_id="abc-123-def-456"
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
        role_id="abc-123-def-456"
    )


@pytest.fixture(name="user_in_db")
def user_in_db_fixture(session: Session, user: User, role_in_db: Role, group_in_db: Group):
    user.role_id = role_in_db.id
    user.group_id = group_in_db.id
    session.add(user)
    session.commit()
    return userrole


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
