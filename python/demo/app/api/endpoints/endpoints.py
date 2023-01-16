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

@router.post("/createService", dependencies=[Depends(verify_webhook)])
async def test(webhook: Webhook):
     action_type = webhook.payload['action']['trigger']
     action_identifier = webhook.payload['action']['identifier']
     properties = webhook.payload['properties']
     blueprint = webhook.context.blueprint

     if action_type == 'CREATE' and action_identifier == 'createService':
        serviceProperties = properties
        run_id = webhook.context.runId
        create_status = port.create_entity(blueprint=blueprint, identifier='',
                                               properties=serviceProperties, run_id=run_id)

        
        action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}
     return {'status': 'SUCCESS'}