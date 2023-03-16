import logging
from fastapi import APIRouter
import random
from clients import port
from schemas.webhook import Webhook
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

createServiceRouter = APIRouter()

@createServiceRouter.post("/createService")
async def createService(webhook: Webhook):
    action_type = webhook.payload['action']['trigger']
    action_identifier = webhook.payload['action']['identifier']
    properties = webhook.payload['properties']
    blueprint = webhook.context.blueprint


    if action_type == 'CREATE' and action_identifier == 'createService':
        run_id = webhook.context.runId

        port.update_run_log(run_id, "Create service started...")
        time.sleep(10)

        body = {
        "identifier": properties.get("name",""),
        "properties": {
            "repository": properties["repository"],
            "replicaCount": properties.get("replicaCount",0),
            "language": properties.get("language", "GO"),
            "communication_method": properties.get("communication_method","GraphQL"),
            "lifecycle": "Experimental",
            "type": "Deployment",
            "jira-issues": 2,
            "chaos-mesh": True,
            "privacy-registered": True,
            "secrets-in-code": False,
            "snyk-vuln": "0",
            "handles-PII": True,
            "number-of-deployments": 0,
            "number-of-pr": 0,
            "number-of-outages": 0,
            "swagger": "https://petstore.swagger.io/v2/swagger.json",
            "encryption-in-rest": False,
            "encryption-in-motion": True,
            "build-success-rate": 0,
            "unit-tests-coverage": 0,
            "tier": "Mission Critical",
            "pr-cycle-time": 1,
            "readme": "# Example Microservice\n\nWelcome to the Example microservice! This service is responsible for\n## Features\n\n## Usage\n\n## Endpoints\n\n- `POST /`\n\n## Dependencies\n\n## Development\n\n## Contributions\n\nWe welcome contributions to the Payment microservice! If you have an idea for a new feature or a bug fix, please open an issue or a pull request.\n\n## License\n\nThe Payment microservice is licensed under the MIT License. See [LICENSE](LICENSE) for more information.",
            "helmChart": "apiVersion: v2\nname: my-chart\nversion: 0.1.0\n\n# This is the chart's description\ndescription: A Helm chart for deploying a Node.js app\n\n# This is the chart's maintainer information\nmaintainer:\n  name: John Doe\n  email: john.doe@example.com\n\n# These are the chart's dependencies\ndependencies:\n  - name: redis\n    version: \"1.0.0\"\n    repository: \"https://kubernetes-charts.storage.googleapis.com\"\n\n# This is the chart's template configuration\ntemplates:\n  - deployment.yaml\n  - service.yaml\n  - ingress.yaml\n" 
            },
        "relations": {
            "domain": properties['domain'],
        },
        "team": properties["team"]
    }
        response = port.create_entity(blueprint=blueprint, identifier='',
                                               body=body, run_id=run_id)

        message = 'Service created successfully' if 200 <= response.status_code <= 299 else 'Service creation failed'
        
        port.log_run_response_details(run_id, response, message)

        action_status = 'SUCCESS' if 200 <= response.status_code <= 299 else 'FAILURE'
        port.update_action(run_id, message, action_status, link="https://github.com/port-labs/repositoryName/actions/runs/" + str(random.randint(1,100)))

        return {'status': action_status}
