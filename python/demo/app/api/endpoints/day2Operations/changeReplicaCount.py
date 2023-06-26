import logging
import time
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

changeReplicaCountRouter = APIRouter()

@changeReplicaCountRouter.post("/scaleReplicaCount")
async def changeReplicaCount(webhook: Webhook):
    
    action_identifier = webhook.action
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if  action_identifier == 'scaleReplicaCount':
        run_id = webhook.context.runId
        
        port.update_run_log(run_id, "🚀 Change Replica Count started.")
        time.sleep(10)
        
        body = {
            "properties": {
                "replicaCount": properties["replicasCount"],
            }
        }
        response = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)

        message = 'Replica count finished successfully' if 200 <= response.status_code <= 299 else 'Replica count update failed'
        port.log_run_response_details(run_id, response, '✅ ' + message if 200 <= response.status_code <= 299 else '❌ ' + message)

        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, "https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}