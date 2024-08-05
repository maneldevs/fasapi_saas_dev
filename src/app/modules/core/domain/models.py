from enum import Enum
from typing import Generic, TypeVar
import uuid
from sqlmodel import Field, SQLModel
from pydantic.generics import GenericModel


T = TypeVar("T", bound=SQLModel)


class DirectionEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class PageParams(SQLModel):
    page: int | None = Field(ge=1, default=1)
    size: int | None = Field(ge=1, default=10)
    order_field: str | None = "id"
    direction: DirectionEnum | None = DirectionEnum.asc


class PageResponse(GenericModel, Generic[T]):
    page: int
    size: int
    total: int
    content: list[T]


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
