from pydantic import BaseModel
from typing import Optional, Any, List


class UserData(BaseModel):
    login: str
    password: str
    email: Optional[str] = None

