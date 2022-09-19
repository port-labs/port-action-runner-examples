from github import Github

from core.config import settings

g = Github(settings.GH_ACCESS_TOKEN)
repo = g.get_repo(f"{settings.GH_ORGANIZATION}/{settings.GH_REPOSITORY}")


def dispatch_workflow(workflow_input: dict, branch_name: str = settings.GH_DEFAULT_BRANCH):
    return repo.get_workflow(settings.GH_WORKFLOW_FILE_NAME).create_dispatch(branch_name, workflow_input)
