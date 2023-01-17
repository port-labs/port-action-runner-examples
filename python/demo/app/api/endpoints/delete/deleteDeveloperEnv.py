import logging
import datetime

from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

deleteDeveloperEnvRouter = APIRouter()

@deleteDeveloperEnvRouter.post("/deleteDeveloperEnv")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DELETE' and action_identifier == 'deleteDeveloperEnv':
        run_id = webhook.context.runId
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
            message = 'Service creation because it has depedencies'
            action_status = 'FAILURE'
            port.update_action(run_id, message, action_status)
            return {'status': action_status}
        if properties['confirm'] is True:
            delete_status = port.delete_entity(blueprint=blueprint, identifier=entity_identifier, run_id=run_id)
            message = 'Service created successfully' if 200 <= delete_status <= 299 else 'Service creation failed'
            action_status = 'SUCCESS' if 200 <= delete_status <= 299 else 'FAILURE'
            port.update_action(run_id, message, action_status)
        else:
            message = 'Service creation cancelled'
            action_status = 'FAILURE'
            port.update_action(run_id, message, action_status)
        return {'status': action_status}
