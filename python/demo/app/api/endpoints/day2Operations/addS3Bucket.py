import time
import logging
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

addS3BucketRouter = APIRouter()

@addS3BucketRouter.post("/addS3Bucket")
async def addS3Bucket(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint

    if action_type == 'DAY-2' and action_identifier == 'addS3Bucket':
        run_id = webhook.context.runId

        message = 'Pr Opened successfully'
        action_status = 'SUCCESS'
        port.update_run_log(run_id, "Add S3 Bucket started.")
        time.sleep(10)

        port.update_action(run_id, message, action_status, link = "https://jenkins.getport.net/job/service/job/mongo/" + str(random.randint(1,100)))
        
        port.update_run_log(run_id, "Add S3 Bucket completed.")
        return {'status': action_status}
