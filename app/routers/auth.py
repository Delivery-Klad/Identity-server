from json import dumps

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.funcs.utils import get_jwt_sub
from app.database import crud, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Identity"])


@router.get("/")
async def login(username: str, password: str, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    data = schemas.UserData(login=username, password=password)
    db_data = crud.login(data, db)
    if not db_data:
        return JSONResponse(status_code=403, content={"result": "Wrong password"})
    if db_data is None:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    pubkey = "exists"
    if db_data.pubkey is None:
        pubkey = "required"
    response = JSONResponse({"res": pubkey,
                             "token": str(authorize.create_refresh_token(dumps({"id": db_data.id,
                                                                                "login": db_data.login})))})
    return response


@router.post("/")  # todo symbols check
async def register(data: schemas.UserData, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    for i in data.login:
        if ord(i) < 33 or ord(i) > 123:
            return JSONResponse(status_code=409, content={"detail": "Unsupported symbols"})
    db_data = crud.register(data, db)
    if not db_data:
        return JSONResponse(status_code=409, content={"detail": "User already exists"})
    pubkey = "exists"
    if db_data.pubkey is None:
        pubkey = "required"
    response = JSONResponse({"res": pubkey,
                             "token": str(authorize.create_refresh_token(dumps({"id": db_data.id,
                                                                                "login": db_data.login})))})
    return response


@router.put("/")
async def update_token(request: Request, authorize: AuthJWT = Depends()):
    data = get_jwt_sub(request)
    response = JSONResponse({"token": str(authorize.create_access_token(dumps({"id": data['id'],
                                                                               "login": data['login']})))})
    return response


@router.patch("/")
async def update_pubkey(key: schemas.UpdateUser, request: Request,
                        db: Session = Depends(get_db)):
    data = get_jwt_sub(request)
    return {"res": crud.update_user(data['id'], key.pubkey, db)}
