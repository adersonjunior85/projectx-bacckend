from fastapi import status
from starlette.exceptions import HTTPException


class RequestFailed(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)


class BadRequest(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail=detail)
