import logging
from fastapi import APIRouter
import random
import time 
from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

restartRunningServiceRouter = APIRouter()

@restartRunningServiceRouter.post("/restart")
async def restartRunningService(webhook: Webhook):
    
    action_identifier = webhook['action']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if  action_identifier == 'restart':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Restart running service started.")
        time.sleep(10)

        action_status = 'SUCCESS'
        port.update_run_log(run_id, "✅ Restart running service completed.")
        port.update_action(run_id, 'Restart finished successfully', action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}