import logging
import datetime
import time
import uuid
import random
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

extendEnvironmentTTLRouter = APIRouter()

@extendEnvironmentTTLRouter.post("/extendEnvironmentTTL")
async def extendEnvironmentTTL(webhook: Webhook):
    
    action_identifier = webhook['action']
    entity_identifier = webhook.payload['entity']['identifier']
    properties = webhook.payload['properties']
    entity = webhook.payload['entity']
    blueprint = webhook.context.blueprint

    if  action_identifier == 'ExtendEnvironmentTTL':
       ttl = properties.get("ttl")
       entityTTL = entity["properties"]["ttl"]
       if(entityTTL == None):
              entityTTL = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

       currentTime = datetime.datetime.strptime(entityTTL,"%Y-%m-%dT%H:%M:%S.%fZ")
       newTime = currentTime
       if ttl == "1 day":
                newTime = currentTime + datetime.timedelta(days=1)
       elif ttl == "1 hour":
                newTime = currentTime + datetime.timedelta(hours=1)
       elif ttl == "4 hours":
                newTime =currentTime + datetime.timedelta(hours=4)
       elif ttl == "3 days":
                newTime = currentTime + datetime.timedelta(days=3)
       elif ttl == "7 days":
                newTime = currentTime + datetime.timedelta(days=7)
       body = {
            "identifier": entity_identifier,
            "properties": {
                "ttl": newTime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            }
         }

       run_id = webhook.context.runId
    
       port.update_run_log(run_id, "🚀 Extend environment TTL started...")
       time.sleep(10)
    
       response = port.patch_entity(blueprint=blueprint, identifier=entity_identifier,
                                               body=body, run_id=run_id)

       message = 'Extend environment TTL finished successfully' if 200 <= response.status_code <= 299 else 'Extend environment TTL failed'
       
       port.log_run_response_details(run_id, response, '✅ ' + message if 200 <= response.status_code <= 299 else '❌ ' + message)

       action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
       port.update_action(run_id, message, action_status, link = "https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))
       return {'status': action_status}