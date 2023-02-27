import logging
import random
from fastapi import APIRouter
import time
from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

redeployImageTagRouter = APIRouter()

@redeployImageTagRouter.post("/redeployImageTag")
async def redeployImageTag(webhook: Webhook):
    time.sleep(15)
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'redeployImageTag':
        run_id = webhook.context.runId
        body = webhook.payload['entity']
        del body['identifier']
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Redeploy finished successfully' if 200 <= create_status <= 299 else 'Redeploy failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}