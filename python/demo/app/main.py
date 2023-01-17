import uvicorn
from fastapi import FastAPI

from api.endpoints.createService import createServiceRouter
from api.endpoints.changeReplicaCount import changeReplicaCountRouter
from api.endpoints.createCloudResource import createCloudResourceRouter
from api.endpoints.restartRunningService import restartRunningServiceRouter
from api.endpoints.lockUnlock import lockUnlockRouter
from api.endpoints.redeployImageTag import redeployImageTagRouter

from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(createServiceRouter, prefix=settings.API_STR)
app.include_router(changeReplicaCountRouter, prefix=settings.API_STR)
app.include_router(createCloudResourceRouter, prefix=settings.API_STR)
app.include_router(restartRunningServiceRouter, prefix=settings.API_STR)
app.include_router(lockUnlockRouter, prefix=settings.API_STR)
app.include_router(redeployImageTagRouter, prefix=settings.API_STR)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3006, reload=True)
