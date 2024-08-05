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
    id: str = Field(default=uuid.uuid4(), primary_key=True)


class GroupCreateCommand(GroupSimpleBase):
    pass


class GroupUpdateCommand(GroupBase):
    pass


class GroupSimpleResponse(GroupSimpleBase):
    id: str


class GroupResponse(GroupBase):
    id: str


class GroupFilter(SQLModel):
    target: str | None = None
