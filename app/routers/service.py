from fastapi import APIRouter


router = APIRouter(prefix="/", tags=["Service"])


@router.get("/ping")
async def ping():
    return "pong"
