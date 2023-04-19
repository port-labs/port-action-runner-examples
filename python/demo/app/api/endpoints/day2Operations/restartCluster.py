import logging
from fastapi import APIRouter
import random
import time 
from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

restartClusterRouter = APIRouter()

@restartClusterRouter.post("/restartCluster")
async def restartCluster(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']

    if action_type == 'DAY-2' and action_identifier == 'restartCluster':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Restart cluster started.")
        time.sleep(10)

        action_status = 'SUCCESS'
        port.update_run_log(run_id, "✅ Restart cluster completed.")
        port.update_action(run_id, 'Restart finished successfully', action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
        return {'status': action_status}

    return {'status': 'SUCCESS'}