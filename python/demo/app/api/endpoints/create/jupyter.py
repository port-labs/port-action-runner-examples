import datetime
import logging
import random
import string
import uuid
import time

from clients import port
from fastapi import APIRouter
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

jupyterRouter = APIRouter()

@jupyterRouter.post("/jupyter")
async def createEnv(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint


    if action_type == 'CREATE' and action_identifier == 'jupyter':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "🚀 Create jupyter started...")
        time.sleep(10)

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
        
            identifier = ''.join(random.choice(string.ascii_letters) for i in range(16))
            serviceRunningBody = {
            "title": service + "-" + "sandbox",
            "identifier": identifier,
            "properties": {
                "locked": False,
                "version": "master." + str(uuid.uuid4()),
                "commitSha": "e7f4329",
                "cpuLimit": 8,
                "memoryLimit": 16,
                "pullRequest": "https://github.com/port-labs/port/pull/master",
                "namespace": "app",
                "podCount": 4,
                "values": "# Application configuration\napp:\n  name: my-app\n  image:\n    repository: my-registry/my-app\n    tag: latest\n  resources:\n    limits:\n      cpu: 100m\n      memory: 128Mi\n    requests:\n      cpu: 50m\n      memory: 64Mi\n  env:\n    - name: ENV\n      value: production\n    - name: PORT\n      value: \"8000\"\n\n# Service configuration\nservice:\n  type: ClusterIP\n  port: 8000\n  targetPort: 8000\n  nodePort: 81000\n\n# Deployment configuration\ndeployment:\n  replicaCount: 1\n  strategy:\n    type: RollingUpdate\n  template:\n    labels:\n      app: my-app\n    spec:\n      containers:\n        - name: my-app\n          image: my-registry/my-app:latest\n          ports:\n            - containerPort: 8000\n          env:\n            - name: ENV\n              value: production\n            - name: PORT\n              value: \"8000\"\n          command: [\"/my-app\"]\n          args: [\"--port=8000\"]\n          resources:\n            limits:\n              cpu: 100m\n              memory: 128Mi\n            requests:\n              cpu: 50m\n              memory: 64Mi",
                "new-relic": "https://chart-embed.service.newrelic.com/herald/b7f0ca98-f82e-4d00-9ac5-01255cfe279d?height=400px&timepicker=true",
                "datadog": "https://p.datadoghq.com/sb/ee7c4d5a-919e-11ed-a723-da7ad0900002-610882095192d0e2e44c2ab031f39c21",
                "logzio": "https://app.logz.io/?embed=true&shareToken=a4807e78-080f-400a-9fee-9cba43141ceb#/dashboard/osd/discover/?_a=(columns%3A!(message)%2Cfilters%3A!()%2Cindex%3A'logzioCustomerIndex*'%2Cinterval%3Aauto%2Cquery%3A(language%3Alucene%2Cquery%3A'')%2Csort%3A!())&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-15m%2Cto%3Anow))&accountIds=842181",
                "replicaCount": 2,
                "envType": "Prod"
            },
            "relations": {
                "environment": "sandbox",
                "service": service,
                "packages-versions": [
                    "express_1_4",
                    "mongodb_1_2",
                    "lodash_2_1",
                    "babel_1_6",
                    "webpack_1_2",
                    "jest_1_2",
                    "eslint_1_6",
                    "dotenv_1_5",
                    "moment_1_9",
                    "pug_1_7",
                    "EcommCore_3_9_6",
                    "OrderProcessor_3_8_5",
                    "InventoryAPI_2_7_3",
                    "CustomerPortal_1_4_5",
                    "AnalyticsTracker_2_7_2"
                    ],
                "cloudResources": [
                "cloud-test-store",
                "data_exporter_test"
                ],
            }
            }
            response = port.create_entity(blueprint='runningService', identifier='',
                                               body=serviceRunningBody, run_id=run_id)
            services.append(identifier)  
            message = 'Running Service created successfully' if 200 <= response.status_code <= 299 else 'Running Service creation failed'

            port.log_run_response_details(run_id, response, '✅ ${message}' if 200 <= response.status_code <= 299 else '❌ ${message}')
            
        body = {
        "identifier": properties["name"],
        "title": properties["name"],
        "properties": {
                "owner": "yupanya414@comcast.biz",
                "status":"Deploying",
                "envUrl": "https://k8s.devenv/" + properties["name"],
                "ttl": ttl.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            },
        "relations": {},
        "team": properties.get("team","")
    }
        response = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= response.status_code <= 299 else 'Service creation failed'

        port.log_run_response_details(run_id, response, '✅ ${message}' if 200 <= response.status_code <= 299 else '❌ ${message}')
        
        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))

        return {'status': action_status}
