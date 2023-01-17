import logging
from fastapi import APIRouter
import random

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

restartRunningServiceRouter = APIRouter()

@restartRunningServiceRouter.post("/restart")
async def restartRunningService(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'restart':
        run_id = webhook.context.runId

        message = 'Restart finished successfully'
        action_status = 'SUCCESS'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}