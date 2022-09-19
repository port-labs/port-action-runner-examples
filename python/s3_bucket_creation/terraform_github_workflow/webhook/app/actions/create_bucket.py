import logging
from typing import Literal, Union
from jinja2 import Environment, FileSystemLoader

from clients import github

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_creation(bucket_name: str, aws_region: str, acl: str,
                  run_id: str) -> Union[Literal['FAILURE'], Literal['SUCCESS']]:
    try:
        rendered_bucket_tf = _render_bucket_tf_template(bucket_name, aws_region, acl)
        new_branch_name = run_id
        github.create_branch(new_branch_name=new_branch_name)
        github.create_file(name=f"tf/{bucket_name}.tf", message=f"Add bucket {bucket_name} terraform file",
                           branch_name=new_branch_name, content=rendered_bucket_tf)
        pr = github.create_pr(title=f"Create new bucket {bucket_name}",
                              body=f"Creating a PR for the new bucket {bucket_name}",
                              head_branch=new_branch_name)
        logger.info(f"init bucket creation of bucket {bucket_name} - success, created PR number: {pr.number}")
        return 'SUCCESS'
    except Exception as err:
        logger.error(f"init bucket creation of bucket {bucket_name} - error: {err}")

    return 'FAILURE'


def _render_bucket_tf_template(bucket_name: str, aws_region: str, acl: str):
    template = Environment(loader=FileSystemLoader("tf_templates/")).get_template("bucket.tf")
    return template.render(region=aws_region, bucket_name=bucket_name, acl=acl)
