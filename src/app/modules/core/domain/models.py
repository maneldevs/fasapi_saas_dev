from typing import Optional
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship


""" Auth """


class Login(SQLModel):
    access_token: str
    token_type: str | None = "bearer"


class LoginCommand(SQLModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)


class LoginResponse(Login):
    pass


""" GroupModule """


class GroupModule(SQLModel, table=True):
    __tablename__ = "group_module"
    group_id: str | None = Field(default=None, primary_key=True, foreign_key="groups.id")
    module_id: str | None = Field(default=None, primary_key=True, foreign_key="modules.id")


""" Group """


class GroupSimpleBase(SQLModel):
    code: str = Field(unique=True, min_length=3)
    webname: str = Field(min_length=3)


class GroupBase(GroupSimpleBase):
    active: bool = True


class Group(GroupBase, table=True):
    __tablename__ = "groups"
    id: str | None = Field(default=None, primary_key=True)

    modules: list["Module"] = Relationship(back_populates="groups", link_model=GroupModule)
    configuration_values: list["ConfigurationValue"] = Relationship(back_populates="group", cascade_delete=True)


class GroupCreateCommand(GroupSimpleBase):
    pass


class GroupUpdateCommand(GroupSimpleBase):
    active: bool


class GroupSimpleResponse(SQLModel):
    id: str | None = None
    code: str | None = None
    webname: str | None = None


class GroupResponse(GroupSimpleResponse):
    active: bool


class GroupResponseWithRels(GroupSimpleResponse):
    active: bool
    modules: list["ModuleResponse"] | None = None
    configuration_values: list["ConfigurationValue"] | None = None


class GroupFilter(SQLModel):
    target: str | None = None


""" RoleMenu """


class RoleMenu(SQLModel, table=True):
    __tablename__ = "role_menu"
    role_id: str | None = Field(default=None, primary_key=True, foreign_key="roles.id")
    menu_id: str | None = Field(default=None, primary_key=True, foreign_key="menus.id")


""" Role """


class RoleBase(SQLModel):
    code: str = Field(unique=True, min_length=3)
    webname: str = Field(min_length=3)


class Role(RoleBase, table=True):
    __tablename__ = "roles"
    id: str | None = Field(default=None, primary_key=True)
    permissions: list["Permission"] = Relationship(back_populates="role", cascade_delete=True)
    menus: list["Menu"] = Relationship(back_populates="roles", link_model=RoleMenu)

    def generate_menu_tree(self):
        response = []
        all_menus = self.menus
        all_menus_ids = [menu.id for menu in all_menus]
        menu_roots = [menu for menu in all_menus if menu.parent is None]
        for menu_root in menu_roots:
            children = [menu_child for menu_child in menu_root.children if menu_child.id in all_menus_ids]
            menu_root.children = children
            response.append(menu_root)
        return response


class RoleCommand(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: str


class RoleFilter(SQLModel):
    target: str | None = None


""" User """


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, min_length=3)
    password: str = Field(min_length=3)
    firstname: str | None = None
    lastname: str | None = None
    active: bool = True
    is_god: bool = False
    group_id: str | None = Field(default=None, foreign_key="groups.id")
    role_id: str | None = Field(default=None, foreign_key="roles.id")

    group: Group | None = Relationship()
    role: Role | None = Relationship()


class UserBaseCommand(SQLModel):
    username: str = Field(min_length=3)
    firstname: str | None = None
    lastname: str | None = None
    group_id: str | None = None
    role_id: str | None = None


class UserCreateCommand(UserBaseCommand):
    password_raw: str = Field(min_length=3)


class UserUpdateCommand(UserBaseCommand):
    password_raw: str | None = None
    active: bool
    is_god: bool


class UserBaseResponse(SQLModel):
    id: str
    username: str


class UserSimpleResponse(UserBaseResponse):
    pass


class UserResponse(UserSimpleResponse):
    firstname: str | None = None
    lastname: str | None = None
    active: bool = True
    is_god: bool = False
    group: GroupResponse | None = None
    role: RoleResponse | None = None


class UserFilter(SQLModel):
    target: str | None = None
    active: Optional[bool] = None
    is_god: bool | None = None
    group_id: str | None = None


class UserWebFilter(SQLModel):
    target: str | None = None
    active: str | None = None
    is_god: str | None = None
    group_id: str | None = None

    def parseToUserFilter(self):
        active = None if self.active == "None" else self.active
        is_god = None if self.is_god == "None" else self.is_god
        return UserFilter(target=self.target, active=active, is_god=is_god, group_id=self.group_id)


""" Modules """


class ModuleBase(SQLModel):
    code: str = Field(unique=True, min_length=3)
    webname: str = Field(min_length=3)


class Module(ModuleBase, table=True):
    __tablename__ = "modules"
    id: str | None = Field(default=None, primary_key=True)

    groups: list[Group] = Relationship(back_populates="modules", link_model=GroupModule)
    resources: list["Resource"] = Relationship(back_populates="module", cascade_delete=True)


class ModuleCommand(ModuleBase):
    pass


class ModuleResponse(ModuleBase):
    id: str


class ModuleFilter(SQLModel):
    target: str | None = None


""" Resources """


class ResourceBase(SQLModel):
    code: str = Field(unique=True, min_length=3)


class Resource(ResourceBase, table=True):
    __tablename__ = "resources"
    id: str | None = Field(default=None, primary_key=True)
    module_id: str = Field(foreign_key="modules.id", ondelete="CASCADE")
    module: Module = Relationship(back_populates="resources")


class ResourceCreateCommand(ResourceBase):
    pass


class ResourceUpdateCommand(ResourceBase):
    module_id: str = Field(min_length=3)


class ResourceSimpleResponse(SQLModel):
    id: str
    code: str


class ResourceResponse(ResourceSimpleResponse):
    module: ModuleResponse


""" Permissions """


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("role_id", "resource_id"),)
    id: str | None = Field(default=None, primary_key=True)
    scope: str | None = None
    scope_owner: str | None = None
    role_id: str = Field(foreign_key="roles.id", ondelete="CASCADE")
    resource_id: str = Field(foreign_key="resources.id", ondelete="CASCADE")
    role: Role = Relationship(back_populates="permissions")
    resource: Resource = Relationship()


class PermissionCreateCommand(SQLModel):
    scope: str | None = None
    scope_owner: str | None = None
    resource_id: str


class PermissionUpdateCommand(SQLModel):
    scope: str | None = None
    scope_owner: str | None = None


class PermissionSimpleResponse(SQLModel):
    id: str
    scope: str | None = None
    scope_owner: str | None = None
    resource: ResourceResponse


class PermissionResponse(PermissionSimpleResponse):
    role: RoleResponse


class PermissionFilter(SQLModel):
    module_id: str | None = None


""" Menu """


class Menu(SQLModel, table=True):
    __tablename__ = "menus"
    id: str | None = Field(default=None, primary_key=True)
    code: str = Field(unique=True, min_length=3)
    link: str | None = None
    module_id: str = Field(foreign_key="modules.id", ondelete="CASCADE")
    module: Module = Relationship()
    parent_id: str | None = Field(foreign_key="menus.id", ondelete="CASCADE", nullable=True)
    parent: Optional["Menu"] | None = Relationship(
        back_populates="children", sa_relationship_kwargs=dict(remote_side="Menu.id")
    )
    children: list["Menu"] = Relationship(back_populates="parent", cascade_delete=True)
    roles: list[Role] = Relationship(back_populates="menus", link_model=RoleMenu)


class MenuCommand(SQLModel):
    code: str = Field(unique=True, min_length=3)
    link: str | None = None
    parent_id: str | None = None
    module_id: str


class MenuSimpleResponse(SQLModel):
    id: str
    code: str
    link: str | None = None
    parent: Optional["MenuSimpleResponse"]
    module: ModuleResponse


class MenuResponse(SQLModel):
    id: str
    code: str
    link: str | None = None
    children: list["MenuResponse"] | None = None
    module: ModuleResponse


""" Configuration """


class Configuration(SQLModel, table=True):
    __tablename__ = "configurations"
    id: str | None = Field(default=None, primary_key=True)
    code: str = Field(unique=True, min_length=3)
    module_id: str | None = Field(default=None, foreign_key="modules.id", ondelete="CASCADE", nullable=True)
    module: Module | None = Relationship()
    configuration_values: list["ConfigurationValue"] = Relationship(back_populates="configuration", cascade_delete=True)


class ConfigurationCommand(SQLModel):
    code: str = Field(unique=True, min_length=3)
    module_id: str | None = None


class ConfigurationResponse(SQLModel):
    id: str
    code: str
    module: Optional[ModuleResponse]


""" Configuration values """


class ConfigurationValue(SQLModel, table=True):
    __tablename__ = "configuration_values"
    __table_args__ = (UniqueConstraint("group_id", "configuration_id"),)
    id: str | None = Field(default=None, primary_key=True)
    value: str = Field(min_length=1)
    group_id: str = Field(foreign_key="groups.id", ondelete="CASCADE")
    group: Group = Relationship()
    configuration_id: str = Field(foreign_key="configurations.id", ondelete="CASCADE")
    configuration: Configuration = Relationship()


class ConfigurationValueCommand(SQLModel):
    configuration_id: str
    value: str = Field(min_length=1)


class ConfigurationValueUpdateCommand(SQLModel):
    value: str = Field(min_length=1)


class ConfigurationValueResponse(SQLModel):
    id: str
    value: str
    configuration: ConfigurationResponse
    group: GroupSimpleResponse


""" Statistics """


class EntitiesCountResponse(SQLModel):
    group_count: int = 0
    role_count: int = 0
    user_count: int = 0
    module_count: int = 0
