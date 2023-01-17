import uvicorn
from fastapi import FastAPI

from api.endpoints.create.createService import createServiceRouter
from api.endpoints.day2Operations.changeReplicaCount import changeReplicaCountRouter
from api.endpoints.create.createCloudResource import createCloudResourceRouter
from api.endpoints.day2Operations.restartRunningService import restartRunningServiceRouter
from api.endpoints.day2Operations.lockUnlock import lockUnlockRouter
from api.endpoints.day2Operations.redeployImageTag import redeployImageTagRouter
from api.endpoints.create.createDeveloperEnv import createDeveloperEnvRouter
from api.endpoints.create.createInHousePackage import createInHousePackageRouter
from api.endpoints.day2Operations.getTemporaryPermissionToCluster import getTempPermissionRouter
from api.endpoints.day2Operations.deployService import deployServiceRouter
from api.endpoints.day2Operations.extendEnvironmentTTL import extendEnvironmentTTLRouter
from api.endpoints.day2Operations.changeOwnership import changeOwnershipRouter
from api.endpoints.day2Operations.rollbackRunningService import rollbackRunningServiceRouter
from api.endpoints.day2Operations.changeOnCall import changeOnCallRouter
from api.endpoints.day2Operations.addS3Bucket import addS3BucketRouter
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
app.include_router(changeOwnershipRouter, prefix=settings.API_STR)
app.include_router(rollbackRunningServiceRouter, prefix=settings.API_STR)
app.include_router(changeOnCallRouter, prefix=settings.API_STR)
app.include_router(addS3BucketRouter, prefix=settings.API_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3006, reload=True)
