import logging
from typing import Literal, Union

from clients import github

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_creation(bucket_name: str, aws_region: str, acl: str,
                  run_id: str) -> Union[Literal['FAILURE'], Literal['SUCCESS']]:
    try:
        workflow_input = {'bucketName': bucket_name, 'awsRegion': aws_region, 'acl': acl, 'runId': run_id}
        success = github.dispatch_workflow(workflow_input)
        if not success:
            raise Exception("Dispatch Github Workflow failed")
        logger.info(f"init bucket creation of bucket {bucket_name} - success")
        return 'SUCCESS'
    except Exception as err:
        logger.error(f"init bucket creation of bucket {bucket_name} - error: {err}")

    return 'FAILURE'
