import logging
import time
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

addMongoDatabaseRouter = APIRouter()

@addMongoDatabaseRouter.post("/addMongoDatabase")
async def addMongoDatabase(webhook: Webhook):
    time.sleep(15)
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'addMongoDatabase':
        run_id = webhook.context.runId
        message = 'Pr Opened successfully'
        action_status = 'SUCCESS'
        port.update_action(run_id, message, action_status, link = "https://jenkins.getport.net/job/service/job/mongo/" + str(random.randint(1,100)))
        return {'status': action_status}
