import logging
from fastapi import APIRouter, Depends
from datetime import datetime
import random
import time

from api.deps import verify_webhook
from clients import port
from core.config import settings
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createCloudResourceRouter = APIRouter()

@createCloudResourceRouter.post("/CreateCloudResource")
async def createCloudResource(webhook: Webhook):
     action_identifier = webhook.action
     properties = webhook.payload['properties']
     blueprint = webhook.context.blueprint

     if  action_identifier == 'CreateCloudResource':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Create cloud resource - " + properties.get("service","") + " started...")
        time.sleep(10)
        
        body = {
        "identifier": properties.get("name"),
        "title": properties.get("name",""),
        "team": properties.get("team",""),
        "properties": {
            "service": properties.get("service",""),
            "region": properties["region"],
            "url": "https://us-east-1.console.gcp.com/rds/" + properties.get("name")
            },
        "relations": {
            "cloud-account": properties["region"]
            }
        }

        response = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= response.status_code <= 299 else 'Service creation failed'

        port.log_run_response_details(run_id, response, '✅ ' + message if 200 <= response.status_code <= 299 else '❌ ' + message)

        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}