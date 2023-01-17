import logging
from fastapi import APIRouter, Depends
from datetime import datetime

from api.deps import verify_webhook
from clients import port
from core.config import settings
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createServiceRouter = APIRouter()

@createServiceRouter.post("/createService")
async def createService(webhook: Webhook):
     action_type = webhook.payload['action']['trigger']
     action_identifier = webhook.payload['action']['identifier']
     properties = webhook.payload['properties']
     blueprint = webhook.context.blueprint

     if action_type == 'CREATE' and action_identifier == 'createService':
        run_id = webhook.context.runId
        body = {
        "identifier": properties.get("name",""),
        "properties": {
            "repository": properties["repository"],
            "replicaCount": properties.get("replicaCount",0),
            "language": properties.get("language", "GO"),
            "communication_method": properties.get("communication_method","GraphQL"),
            "lifecycle": "Experimental",
            "type": "Deployment",
            "helmChart": "apiVersion: v2\nname: my-chart\nversion: 0.1.0\n\n# This is the chart's description\ndescription: A Helm chart for deploying a Node.js app\n\n# This is the chart's maintainer information\nmaintainer:\n  name: John Doe\n  email: john.doe@example.com\n\n# These are the chart's dependencies\ndependencies:\n  - name: redis\n    version: \"1.0.0\"\n    repository: \"https://kubernetes-charts.storage.googleapis.com\"\n\n# This is the chart's template configuration\ntemplates:\n  - deployment.yaml\n  - service.yaml\n  - ingress.yaml\n" 
            },
        "relations": {
            "domain": properties['domain'],
        },
        "team": properties["team"]
    }
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= create_status <= 299 else 'Service creation failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)
        return {'status': action_status}
