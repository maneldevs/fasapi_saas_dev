from sqlmodel import Field, SQLModel, Relationship


""" Group """


class GroupSimpleBase(SQLModel):
    code: str = Field(unique=True)
    webname: str


class GroupBase(GroupSimpleBase):
    active: bool = True


class Group(GroupBase, table=True):
    __tablename__ = "groups"
    id: str | None = Field(default=None, primary_key=True)


class GroupCreateCommand(GroupSimpleBase):
    pass


class GroupUpdateCommand(GroupSimpleBase):
    active: bool


class GroupSimpleResponse(GroupSimpleBase):
    id: str


class GroupResponse(GroupSimpleBase):
    id: str
    active: bool


class GroupFilter(SQLModel):
    target: str | None = None


""" Role """


class RoleBase(SQLModel):
    code: str = Field(unique=True)
    webname: str


class Role(RoleBase, table=True):
    __tablename__ = "roles"
    id: str | None = Field(default=None, primary_key=True)


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
    username: str = Field(unique=True)
    password: str
    firstname: str | None = None
    lastname: str | None = None
    active: bool = True
    is_god: bool = False
    group_id: str | None = Field(default=None, foreign_key="groups.id")
    role_id: str | None = Field(default=None, foreign_key="roles.id")

    group: Group | None = Relationship()
    role: Role | None = Relationship()


class UserBaseCommand(SQLModel):
    username: str
    firstname: str | None = None
    lastname: str | None = None
    group_id: str | None = None
    role_id: str | None = None


class UserCreateCommand(UserBaseCommand):
    password_raw: str


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
    active: bool | None = None
    is_god: bool | None = None
    group_id: str | None = None
