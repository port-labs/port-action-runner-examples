import logging
import time
from fastapi import APIRouter
import random

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lockUnlockRouter = APIRouter()

@lockUnlockRouter.post("/lock")
async def lockUnlock(webhook: Webhook):
    
    action_identifier = webhook['action']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if  action_identifier == 'lock':
        run_id = webhook.context.runId
    
        port.update_run_log(run_id, "🚀 Lock started.")
        time.sleep(10)

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
       
        response = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)

        message = 'lock finished successfully' if 200 <= response.status_code <= 299 else 'lock failed'
        
        port.log_run_response_details(run_id, response, '✅ ' + message if 200 <= response.status_code <= 299 else '❌ ' + message)
        
        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}