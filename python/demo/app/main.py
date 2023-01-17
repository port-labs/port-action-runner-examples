import uvicorn
from fastapi import FastAPI

from api.endpoints.createService import createServiceRouter
from api.endpoints.changeReplicaCount import changeReplicaCountRouter
from api.endpoints.createCloudResource import createCloudResourceRouter
from api.endpoints.restartRunningService import restartRunningServiceRouter
from api.endpoints.lockUnlock import lockUnlockRouter
from api.endpoints.redeployImageTag import redeployImageTagRouter
from api.endpoints.createDeveloperEnv import createDeveloperEnvRouter
from api.endpoints.createInHousePackage import createInHousePackageRouter
from api.endpoints.getTemporaryPermissionToCluster import getTempPermissionRouter
from api.endpoints.deployService import deployServiceRouter
from api.endpoints.extendEnvironmentTTL import extendEnvironmentTTLRouter
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
app.include_router(getTempPermissionRouter, prefix=settings.API_STR)
app.include_router(createDeveloperEnvRouter, prefix=settings.API_STR)
app.include_router(createInHousePackageRouter, prefix=settings.API_STR)
app.include_router(deployServiceRouter, prefix=settings.API_STR)
app.include_router(extendEnvironmentTTLRouter, prefix=settings.API_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3006, reload=True)
