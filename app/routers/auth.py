from fastapi import APIRouter, Request, Cookie, Depends
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from typing import Optional

from app.funcs.utils import get_jwt_sub
from app.database import crud, schemas
from app.dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Identity"])


@router.get("/", status_code=200)
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
    response = JSONResponse({"res": pubkey}, status_code=200)
    response.set_cookie("token", str(authorize.create_refresh_token(db_data.login)), secure=True, httponly=True, samesite="None")
    return response


@router.post("/", status_code=201)  # todo symbols check
async def register(data: schemas.UserData, authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_data = crud.register(data, db)
    if not db_data:
        return JSONResponse(status_code=409, content={"detail": "User already exists"})
    pubkey = "exists"
    if db_data.pubkey is None:
        pubkey = "required"
    response = JSONResponse({"res": pubkey}, status_code=200)
    response.set_cookie("token", str(authorize.create_refresh_token(db_data.login)), secure=True, httponly=True, samesite="None")
    return response


@router.delete("/", status_code=200)
async def logout(request: Request, token: Optional[str] = Cookie(None)):
    data = get_jwt_sub(request, token)
    if data is None:
        return JSONResponse(status_code=403)
    response = JSONResponse(status_code=200)
    response.delete_cookie("token")
    return response
