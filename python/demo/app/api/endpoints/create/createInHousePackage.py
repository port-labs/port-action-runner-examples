import logging
import datetime
import random 
import time

from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createInHousePackageRouter = APIRouter()

@createInHousePackageRouter.post("/createPackage")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint


    if action_type == 'CREATE' and action_identifier == 'createPackage':
        run_id = webhook.context.runId
        
        port.update_run_log(run_id, "🚀 Create package started...")
        time.sleep(10)

        body = {
        "identifier": properties.get("name", ""),
        "title": properties.get("name", ""),
        "properties": {
                "repository": properties.get("repository", ""),
                "language": properties.get("language", "Python"),
                "envUrl": "https://k8s.devenv/" + properties.get("name", ""),
                "github-url": "https://github.com/port-labs/" + properties.get("name", ""),
                "inHouse": True,
            },
        "relations": {},
        "team": properties.get("team","")
    }
        response = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= response.status_code <= 299 else 'Service creation failed'
        
        port.log_run_response_details(run_id, response, '✅' + message if 200 <= response.status_code <= 299 else '❌' + message)

        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))

        return {'status': action_status}
