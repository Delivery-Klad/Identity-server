import uvicorn

from app.dependencies import get_settings


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("app.main:app")
