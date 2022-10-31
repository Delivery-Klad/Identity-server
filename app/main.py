from random import randint
from secrets import token_hex

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from app.tags import tags_metadata
from app.routers import auth, service
from app.database.database import SessionLocal
from app.dependencies import get_settings

settings = get_settings()
swagger_url = token_hex(randint(10, 15))
app = FastAPI(title="Identity server", version="0.1", redoc_url=None, openapi_tags=tags_metadata)
app.include_router(service.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "https://chat.c1oud.ru", "https://dev.c1oud.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.secret


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": exc.message})


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
