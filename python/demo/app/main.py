import uvicorn
from fastapi import FastAPI

from api.endpoints.createService import createServiceRouter
from api.endpoints.changeReplicaCount import changeReplicaCountRouter

from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(createServiceRouter, prefix=settings.API_STR)
app.include_router(changeReplicaCountRouter, prefix=settings.API_STR)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3006, reload=True)