
import logging
from fastapi import APIRouter
import random
from clients import port
from schemas.webhook import Webhook
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createIssueRouter = APIRouter()

@createIssueRouter.post("/createIssue")
async def createService(webhook: Webhook):
    
    action_identifier = webhook.action
    if  action_identifier == 'createIssue':
        run_id = webhook.context.runId
        port.update_run_log(run_id, "🚀 Create issue started.")
        time.sleep(10)

        action_status = 'SUCCESS'
        port.update_run_log(run_id, "✅ Create issue service completed.")
        port.update_action(run_id, 'Restart finished successfully', action_status, link="https://demo.atlassian.net/jira/browse/DEMO-" + str(random.randint(1,100)))
        return {'status': action_status}
