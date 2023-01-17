import logging
from fastapi import APIRouter
import random

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lockUnlockRouter = APIRouter()

@lockUnlockRouter.post("/lock")
async def lockUnlock(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'lock':
        desiredState = properties["state"]

        if desiredState == "Locked":
            body = {
                "properties": {
                    "locked": True,
                }
            }
        elif desiredState == "Unlocked":
            body = {
                "properties": {
                    "locked": False,
                }
            }
        run_id = webhook.context.runId
  
        patch_status = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)

        message = 'lock finished successfully' if 200 <= patch_status <= 299 else 'lock failed'
        action_status = 'SUCCESS' if 200 <= patch_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}