from enum import Enum
from typing import Generic, TypeVar
from sqlmodel import Field, SQLModel
from sqlmodel.sql.expression import SelectOfScalar


T = TypeVar("T", bound=SQLModel)


class DirectionEnum(str, Enum):
    asc = "asc"
    desc = "desc"


class PageParams(SQLModel):
    page: int | None = Field(ge=1, default=1)
    size: int | None = Field(ge=1, default=10)
    order_field: str | None = "id"
    direction: DirectionEnum | None = DirectionEnum.asc


class PageResponse(SQLModel, Generic[T]):
    page: int
    size: int
    total: int
    content: list[T]


class Paginator(Generic[T]):

    def __init__(self, entity: T) -> None:
        self.entity = entity

    def paginate_query(self, stmt: SelectOfScalar[T], page_params: PageParams) -> SelectOfScalar[T]:
        stmt = self.__apply_order(stmt, page_params.order_field, page_params.direction)
        stmt = self.__apply_page(stmt, page_params.page, page_params.size)
        return stmt

    def __apply_order(self, stmt: SelectOfScalar[T], order_field: str, direction: DirectionEnum) -> SelectOfScalar[T]:
        order_column = getattr(self.entity, order_field)
        if direction is DirectionEnum.desc:
            order_column = order_column.desc()
        return stmt.order_by(order_column)

    def __apply_page(self, stmt: SelectOfScalar[T], page: int, size: int) -> SelectOfScalar[T]:
        return stmt.offset((page - 1) * size).limit(size)
