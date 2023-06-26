import logging
from fastapi import APIRouter, Depends
from datetime import datetime

from actions import create_bucket
from api.deps import verify_webhook
from clients import port
from core.config import settings
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
        action_status = create_bucket.create(bucket_name, aws_region, acl)
        message = f"The action status after creating bucket is {action_status}"
        if action_status == 'SUCCESS':
            entity_properties = {'acl': acl,
                                 'awsRegion': aws_region,
                                 'createdDate': datetime.now().isoformat("T") + "Z",
                                 'S3Link': settings.AWS_S3_BUCKET_LINK.format(bucket_name=bucket_name)}
            create_status = port.create_entity(blueprint=settings.PORT_S3_BUCKET_BLUEPRINT, identifier=bucket_name,
                                               properties=entity_properties, run_id=run_id)
            action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
            message = f"{message}, after creating entity is {action_status}"

        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}

    return {'status': 'IGNORED'}
