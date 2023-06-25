import logging
from fastapi import APIRouter
import uuid
import random
import time

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rollbackRunningServiceRouter = APIRouter()

@rollbackRunningServiceRouter.post("/rollback")
async def rollbackRunningService(webhook: Webhook):
    
    action_identifier = webhook['action']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if  action_identifier == 'rollback':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Rollback running service started.")
        time.sleep(10)

        body = {
            "properties": {
                "version": "master." + str(uuid.uuid4())
            }
        }

        response = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)
                                      
        message = 'RollBack finished successfully' if 200 <= response.status_code <= 299 else 'RollBack failed'

        port.log_run_response_details(run_id, response, '✅ ' + message if 200 <= response.status_code <= 299 else '❌ ' + message)

        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link = "https://jenkins.getport.net/job/service/job/mongo/" + str(random.randint(1,100)))
        return {'status': action_status}