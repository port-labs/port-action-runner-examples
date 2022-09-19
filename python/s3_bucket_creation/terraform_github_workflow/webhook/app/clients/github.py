from github import Github

from core.config import settings

g = Github(settings.GH_ACCESS_TOKEN)
repo = g.get_repo(f"{settings.GH_ORGANIZATION}/{settings.GH_REPOSITORY}")


def create_branch(new_branch_name: str, source_branch_name=settings.GH_DEFAULT_BRANCH):
    source_branch = repo.get_branch(source_branch_name)
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=source_branch.commit.sha)


def create_file(name: str, message: str, branch_name: str, content: str):
    repo.create_file(name, message, branch=branch_name, content=content)


def create_pr(title: str, body: str, head_branch: str, base_branch: str = settings.GH_DEFAULT_BRANCH):
    return repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)
