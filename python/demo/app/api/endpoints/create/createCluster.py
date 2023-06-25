import logging
from fastapi import APIRouter
import random
from clients import port
from schemas.webhook import Webhook
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createClusterRouter = APIRouter()

@createClusterRouter.post("/createCluster")
async def createService(webhook: Webhook):
    
    action_identifier = webhook.action
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint


    if  action_identifier == 'createCluster':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Create cluster started...")
        time.sleep(10)

        body = {
        "identifier": properties.get("name",""),
        "properties": {
            },
        "relations": {
            "cloud-account": properties['cloudAccount'],
        },
        "team": properties["team"]
    }
        response = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= response.status_code <= 299 else 'Service creation failed'
        
        port.log_run_response_details(run_id, response, '✅ ' + message if 200 <= response.status_code <= 299 else '❌ ' + message)

        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))

        return {'status': action_status}
