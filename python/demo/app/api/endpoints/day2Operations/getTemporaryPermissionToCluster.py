import logging
import time
from fastapi import APIRouter
import datetime
import random
from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

getTempPermissionRouter = APIRouter()

@getTempPermissionRouter.post("/getTemporaryPermission")
async def getTempPermission(webhook: Webhook):
    time.sleep(15)
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'getTemporaryPermission':
        run_id = webhook.context.runId
        run_id = webhook.context.runId
        ttl = properties.get("ttl")

        if ttl == "1 day":
            ttl = datetime.datetime.now() + datetime.timedelta(days=1)
        elif ttl == "1 hour":
            ttl = datetime.datetime.now() + datetime.timedelta(hours=1)
        elif ttl == "4 hours":
            ttl = datetime.datetime.now() + datetime.timedelta(hours=4)
        elif ttl == "3 days":
            ttl = datetime.datetime.now() + datetime.timedelta(days=3)
        elif ttl == "7 days":
            ttl = datetime.datetime.now() + datetime.timedelta(days=7)
        
        relations = {}
        icon = ''

        if blueprint == 'k8s-cluster':
            icon = "Cluster"
            relations = {
                "k8s-cluster": entity_identifier,
            }
        elif blueprint == 'cloudResource':
            icon = 'Lock'
            relations = {
                "cloudResource": entity_identifier,
            }

        body = {
        "title": "Ibrahim-Troubleshooting",
        "icon": icon,
        "properties": {
                "user": "ibrahimrotich@club-internet.com",
                "status": "Pending",
                "reason": properties.get("reason",""),
                "ttl": ttl.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
        "relations": relations,
    }
        create_status = port.create_entity(blueprint='permission', identifier='',body=body, run_id=run_id)

        message = 'Get temporary permission for cluster finished successfully' if 200 <= create_status <= 299 else 'Get temporary permission for cluster failed'
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, "https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}