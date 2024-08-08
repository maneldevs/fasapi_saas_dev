import pytest
from sqlmodel import Session

from src.app.modules.core.domain.group_service import GroupService
from src.app.modules.core.domain.models import Group, GroupCreateCommand, GroupUpdateCommand, Role, RoleCommand
from src.app.main import app


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
