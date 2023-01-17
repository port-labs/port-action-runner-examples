import logging
import datetime

from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createDeveloperEnvRouter = APIRouter()

@createDeveloperEnvRouter.post("/CreateEnvironment")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint


    if action_type == 'CREATE' and action_identifier == 'CreateEnvironment':
        run_id = webhook.context.runId
        ttl = properties.get("ttl")
        if ttl == "1 day":
            ttl = datetime.datetime.now() + datetime.timedelta(days=1)
        elif ttl == "1 hour":
            ttl = datetime.datetime.now() + datetime.timedelta(hours=1)
        elif ttl == "4 hours":
            ttl = datetime.datetime.now() + datetime.timedelta(hours=4)
        elif ttl == "3 days":
            ttl = datetime.datetime.now() + datetime.timedelta(days=3)
        elif ttl == "7 days":
            ttl = datetime.datetime.now() + datetime.timedelta(days=7)
        
        body = {
        "identifier": properties["name"],
        "title": properties["name"],
        "properties": {
                "owner": "yupanya414@comcast.biz",
                "status":"Deploying",
                "envUrl": "https://k8s.devenv/" + properties["name"],
                "ttl": ttl.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
        "relations": {
            "runningServices": properties['services'],
        },
        "team": properties.get("team","")
    }
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= create_status <= 299 else 'Service creation failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)

        return {'status': action_status}
