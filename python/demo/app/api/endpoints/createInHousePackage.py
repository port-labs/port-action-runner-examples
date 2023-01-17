import logging
import datetime

from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createInHousePackageRouter = APIRouter()

@createInHousePackageRouter.post("/createPackage")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint


    if action_type == 'CREATE' and action_identifier == 'createPackage':
        run_id = webhook.context.runId
        
        body = {
        "identifier": properties.get("name", ""),
        "title": properties.get("name", ""),
        "properties": {
                "repository": properties.get("repository", ""),
                "language": properties.get("language", "Python"),
                "envUrl": "https://k8s.devenv/" + properties["name"],
                "github-url": "https://github.com/port-labs/" + properties["name"],
                "inHouse": True,
            },
        "relations": {},
        "team": properties.get("team","")
    }
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= create_status <= 299 else 'Service creation failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)

        return {'status': action_status}
