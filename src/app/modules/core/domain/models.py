from sqlmodel import Field, SQLModel


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


""" Roles """


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
