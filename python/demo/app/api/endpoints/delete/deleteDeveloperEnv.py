import logging
import datetime
import random
import time
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

deleteDeveloperEnvRouter = APIRouter()

@deleteDeveloperEnvRouter.post("/deletedveloperEnv")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DELETE' and action_identifier == 'DeleteEnvironment':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "Developer Env deletion started.")
        time.sleep(10)

        if (entity_identifier in [
                "test-anton",
                "feature-b-dev-env",
                "test-a-dev-env",
                "test-francisca-1",
                "test-ryoko",
                "test-c-dev-env",
                "test-francisca-2",
                "check-bugfix-2451",
                "check-bugfix-123",
                "feature-a-dev-env",
                "test-shizuko",
            ]):
            message = 'Developer Env deletion because it has depedencies'
            action_status = 'FAILURE'
            port.update_action(run_id, message, action_status)
            return {'status': action_status}

        response = port.delete_entity(blueprint=blueprint, identifier=entity_identifier, run_id=run_id)
        message = 'Developer Env deleted successfully' if 200 <= response.status_code <= 299 else 'Developer Env deletion failed'
        
        port.log_run_response_details(run_id, response, message)
        
        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link = "https://jenkins.getport.net/job/service/job/mongo/" + str(random.randint(1,100)))

        return {'status': action_status}
