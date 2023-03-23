import logging
import time
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
        
        port.update_run_log(run_id, "🚀 Change Ownership started.")
        time.sleep(10)

        body = {
            "team": properties.get("team",""),
        }
        response = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)

        message = 'Replica count finished successfully' if 200 <= response.status_code <= 299 else 'Replica count update failed'
        port.log_run_response_details(run_id, response, '✅' + message if 200 <= response.status_code <= 299 else '❌' + message)
        
        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link='https://getport-io.pagerduty.com/service-directory/PAS5I1V')
        return {'status': action_status}

    return {'status': 'SUCCESS'}