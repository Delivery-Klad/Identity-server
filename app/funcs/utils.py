from json import loads

from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException


def get_jwt_sub(request, cookie: str = None):
    if cookie is not None:
        request.headers.__dict__["_list"].append(("authorization".encode(), f"Bearer {cookie}".encode()))
    authorize = AuthJWT(request)
    try:
        return loads(authorize.get_jwt_subject())
    except Exception as e:
        raise HTTPException(status_code=403)
