import logging
import datetime
import random
from fastapi import APIRouter
import time

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

deleteRepoRouter = APIRouter()

@deleteRepoRouter.post("/deleteRepo")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DELETE' and action_identifier == 'deleteRepo':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Repo deletion started.")
        time.sleep(10)

        if (entity_identifier in [
                "subscription",
                "shipping",
                "inventory",
                "analytics",
                "order",
                "frontend",
                "authentication",
                "payment",
                "recommendation",
                "authorization",
                "fraud-detection",
                "wish-list",
                "load-generator",
                "shipping",
                "pricing",
                "currency",
                "rating",
                "ads",
                "checkout"
            ]):
            message = 'Service deletion failed because it has dependencies'
            action_status = 'FAILURE'
            response = port.update_action(run_id, message, action_status)
            port.log_run_response_details(run_id, response, '❌'.format(message))
            
            return {'status': action_status}
        if properties['confirm'] is True:
            response = port.delete_entity(blueprint=blueprint, identifier=entity_identifier, run_id=run_id)
            message = 'Service deleted successfully' if 200 <= response.status_code <= 299 else 'Service deletion failed'

            port.log_run_response_details(run_id, response, '✅'.format(message) if 200 <= response.status_code <= 299 else '❌'.format(message))
            
            action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
            port.update_action(run_id, message, action_status, link = "https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        else:
            message = 'Service deletion cancelled'
            port.log_run_response_details(run_id, response, '❌'.format(message))

            action_status = 'FAILURE'
            port.update_action(run_id, message, action_status)
        return {'status': action_status}
