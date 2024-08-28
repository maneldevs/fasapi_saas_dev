from enum import Enum
from typing import Generic, TypeVar
from pydantic import TypeAdapter
from sqlmodel import Field, SQLModel
from sqlmodel.sql.expression import SelectOfScalar


T = TypeVar("T", bound=SQLModel)
U = TypeVar("U", bound=SQLModel)
V = TypeVar("V", bound=SQLModel)


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


class PageParser(Generic[T, U, V]):

    def __init__(self, list_origin: list[T], target_class: type):
        self.list_origin = list_origin
        self.target_class = target_class

    def parse_list(self) -> list[U]:
        type_adapter = TypeAdapter(list[self.target_class])
        return type_adapter.validate_python(self.list_origin)

    def generate_page_response(self, page: int, size: int, total: int) -> PageResponse[U]:
        list_target = self.parse_list()
        return PageResponse(page=page, size=size, total=total, content=list_target)

    def generate_web_context(self, page_params: PageParams, total: int, filter: V, msg: str, msg_type: str = "success"):
        list_target = self.parse_list()
        page_response = PageResponse(page=page_params.page, size=page_params.size, total=total, content=list_target)
        context = page_response.model_dump()
        context |= filter.model_dump()
        params = (
            f"&size={page_params.size}&order_field={page_params.order_field}&direction={page_params.direction.value}"
        )
        filter_dict = filter.model_dump(exclude_unset=True, exclude_none=True)
        for k, v in filter_dict.items():
            params += f"&{k}={v}"
        context |= {"query_params": params}
        context |= {"msg": msg, "type": msg_type}
        return context
