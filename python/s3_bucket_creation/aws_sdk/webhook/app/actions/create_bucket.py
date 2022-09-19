import logging
from typing import Literal, Union

from clients import aws_s3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create(bucket_name: str, aws_region: str, acl: str) -> Union[Literal['FAILURE'], Literal['SUCCESS']]:
    try:
        aws_s3.create_bucket(bucket_name, aws_region, acl)
        logger.info(f"create bucket {bucket_name} - success")
        return 'SUCCESS'
    except Exception as err:
        logger.error(f"create bucket {bucket_name} - error: {err}")

    return 'FAILURE'
