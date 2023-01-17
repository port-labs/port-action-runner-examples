import logging
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createServiceRouter = APIRouter()

@createServiceRouter.post("/createService")
async def test(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'CREATE' and action_identifier == 'createService':
        run_id = webhook.context.runId
        body = {
        "properties": {
            "repository": properties["repository"],
            "replicaCount": properties["replicaCount"],
            "team": properties["team"],
            "domain": properties["domain"],
            "language": properties["language"],
            "communication_method": properties["communication_method"],
            "db":  properties["db"],
            "queue": properties["queue"],
            "description": properties["description"]
            },
        "relations": {
            "domain": properties['domain'],
        }
    }
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= create_status <= 299 else 'Service creation failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}
    return {'status': 'SUCCESS'}