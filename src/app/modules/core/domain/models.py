import uuid
from sqlmodel import Field, SQLModel


''' Group '''


class GroupSimpleBase(SQLModel):
    code: str = Field(unique=True)
    webname: str


class GroupBase(GroupSimpleBase):
    active: bool = True


class Group(GroupBase, table=True):
    __tablename__ = "groups"
    id: str | None = Field(default=str(uuid.uuid4()), primary_key=True)


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
