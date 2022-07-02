from fastapi_jwt_auth import AuthJWT


def get_jwt_sub(request, cookie: str):
    request.headers.__dict__["_list"]\
        .append(("authorization".encode(), f"Bearer {cookie}".encode()))
    authorize = AuthJWT(request)
    try:
        return authorize.get_jwt_subject()
    except Exception as e:
        return None
