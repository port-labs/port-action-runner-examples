import logging
from fastapi import APIRouter, Depends

from actions import create_bucket
from api.deps import verify_webhook
from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/bucket", dependencies=[Depends(verify_webhook)])
async def handle_create_bucket_webhook(webhook: Webhook):
    logger.info(f"Webhook body: {webhook}")
    
    action_identifier = webhook.action
    properties = webhook.payload['properties']

    if  action_identifier == 'CreateBucket':
        bucket_name = properties['bucket-name']
        aws_region = properties['aws-region']
        acl = properties['acl']
        run_id = webhook.context.runId

        logger.info(f"Create new bucket, name: {bucket_name}")
        action_status = create_bucket.init_creation(bucket_name, aws_region, acl, run_id)
        message = f"The action status after init bucket creation is {action_status}"
        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}

    return {'status': 'IGNORED'}
