import logging
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

changeOwnershipRouter = APIRouter()

@changeOwnershipRouter.post("/changeOwnership")
async def changeReplicaCount(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'changeOwnership':
        run_id = webhook.context.runId
        body = {
            "team": properties.get("team",""),
        }
        patch_status = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)

        message = 'Replica count finished successfully' if 200 <= patch_status <= 299 else 'Replica count update failed'
        action_status = 'SUCCESS' if 200 <= patch_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)
        return {'status': action_status}

    return {'status': 'SUCCESS'}