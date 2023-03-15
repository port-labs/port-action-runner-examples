import logging
import time
import datetime
import uuid
import random
from fastapi import APIRouter

from clients import port
from schemas.webhook import Webhook

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

deployServiceRouter = APIRouter()

@deployServiceRouter.post("/deployService")
async def deployService(webhook: Webhook):
    time.sleep(10)
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    entity = webhook.payload['entity']
    blueprint = "runningService"


    if action_type == 'DAY-2' and action_identifier == 'deploy':
        run_id = webhook.context.runId
        
        port.update_run_log(run_id, "Deploy Service started.")
        time.sleep(5)

        body = {
        "identifier": entity['identifier'] + "-" + properties.get("environment","dev"),
        "title": entity['identifier'] + "-" + properties.get("environment","dev"),
        "properties": {
            "locked": False,
            "version": properties["branch"],
            "commitSha": "e7f4329",
            "cpuLimit": 8,
            "memoryLimit": 16,
            "pullRequest": "https://github.com/port-labs/port/pull/" + properties["branch"],
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
            "k8s-cluster": properties.get("environment","dev"),
            "service": entity['identifier'],
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
        },
        "team": properties.get("team","")
    }
        response = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= response.status_code <= 299 else 'Service creation failed'
        
        port.log_run_response_details(run_id, response, message)
        
        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        if (action_status == 'SUCCESS'):
            deployment = {
                "title": entity['identifier'] + "-" + properties.get("environment","dev"),
                "properties": {
                "user": "michaelmolina@shaw.org",
                "status": "Success",
                "duration": "7 min 13 sec",
                "version": properties["branch"] + '.' + uuid.uuid4(),
                "commitSha": "e7f4329",
                "jiraTicket": "https://devportal.atlassian.jira.net/browse/" + properties["branch"],
                "service": entity['identifier'],
                "workflowUrl": "https://github.com/port-labs/Port/actions/runs/e605d19",
                "deployBranchUrl": "https://github.com/port-labs/Port/tree/bugfix.c7c4b6d8-40fd-4263-8674-2158f8afd0a6.2023-01-06_22-37-38.c83dea1",
                "sentryRelease": "https://sentry.io/organizations/getport/releases/pricing/?project=e605d19"
                    },
                "relations": {
                    "runningService": entity['identifier'] + "-" + properties.get("environment","dev"),
                    }
                }

            response = port.create_entity(blueprint='deployment', identifier='',
                                               body=deployment, run_id=run_id)
            
            message = 'Deployment created successfully' if 200 <= response.status_code <= 299 else 'Deployment creation failed'

            port.log_run_response_details(run_id, response, message)

        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))

        return {'status': action_status}
