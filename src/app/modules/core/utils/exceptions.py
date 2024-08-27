class BaseError(Exception):
    def __init__(self, type: str, msg: str, status_code: int, original_exception: Exception = None) -> None:
        self.type = type
        self.msg = msg
        self.status_code = status_code
        self.original_exception = original_exception


class EntityAlreadyExistsError(BaseError):
    def __init__(self, msg: str = "Entity already exists", original_exception: Exception = None) -> None:
        super().__init__(type="database", msg=msg, status_code=400, original_exception=original_exception)


class EntityRelationshipExistsError(BaseError):
    def __init__(self, msg: str = "Entity has dependants", original_exception: Exception = None) -> None:
        super().__init__(type="forbidden", msg=msg, status_code=400, original_exception=original_exception)


class EntityNotFoundError(BaseError):
    def __init__(self, msg: str = "Entity not found", original_exception: Exception = None) -> None:
        super().__init__(type="not found", msg=msg, status_code=404, original_exception=original_exception)


class CredentialsError(BaseError):
    def __init__(self, msg: str = "Incorrect username or password", original_exception: Exception = None) -> None:
        super().__init__(type="credentials", msg=msg, status_code=401, original_exception=original_exception)


class TokenInvalidError(BaseError):
    def __init__(self, msg: str = "Token invalid", original_exception: Exception = None) -> None:
        super().__init__(type="unathenticated", msg=msg, status_code=401, original_exception=original_exception)


class ForbiddenError(BaseError):
    def __init__(self, msg: str = "Forbidden", original_exception: Exception = None) -> None:
        super().__init__(type="forbidden", msg=msg, status_code=403, original_exception=original_exception)
