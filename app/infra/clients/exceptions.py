from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class RouteRequestFailed(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)


class KeyExistsError(Exception):
    def __init__(self, detail: str = "Error checking if key exists"):
        super().__init__(detail)


class GetRouteError(Exception):
    def __init__(self, detail: str = "Error getting route"):
        super().__init__(detail)


class SetExpirationError(Exception):
    def __init__(self, detail: str = "Error setting expiration"):
        super().__init__(detail)


class SaveRouteError(Exception):
    def __init__(self, detail: str = "Error saving route"):
        super().__init__(detail)
