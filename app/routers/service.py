from fastapi import APIRouter


router = APIRouter(tags=["Service"])


@router.get("/ping")
async def ping():
    return "pong"
