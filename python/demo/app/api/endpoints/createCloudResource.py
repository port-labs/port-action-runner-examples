import logging
from fastapi import APIRouter, Depends
from datetime import datetime

from api.deps import verify_webhook
from clients import port
from core.config import settings
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createCloudResourceRouter = APIRouter()

@createCloudResourceRouter.post("/CreateCloudResource")
async def createCloudResource(webhook: Webhook):
     action_type = webhook.payload['action']['trigger']
     action_identifier = webhook.payload['action']['identifier']
     properties = webhook.payload['properties']
     blueprint = webhook.context.blueprint

     if action_type == 'CREATE' and action_identifier == 'CreateCloudResource':
        run_id = webhook.context.runId
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
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= create_status <= 299 else 'Service creation failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)
        return {'status': action_status}