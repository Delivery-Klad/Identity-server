from pydantic import BaseModel
from typing import Optional


class UserData(BaseModel):
    login: str
    password: str
    email: Optional[str] = None


class UpdateUser(BaseModel):
    pubkey: Optional[str] = None
