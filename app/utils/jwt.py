from jose import jwt


def _remove_jwt_bearer(token: str) -> str:
    if "Bearer" in token:
        return token.split(" ")[1]
    return token


def decode_jwt(
    token: str,
    key: str = "secret",
    algorithms: list = None,
    options: dict = None,
):
    if not token:
        return
    if not algorithms:
        algorithms = ["RS256"]
    if not options:
        options = {"verify_signature": False}
    try:
        token = _remove_jwt_bearer(token=token)
        claims = jwt.decode(
            token=token, key=key, algorithms=algorithms, options=options
        )
        return claims
    except jwt.JWTError:
        return token
