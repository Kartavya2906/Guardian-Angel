from git import Repo
import os

def clone_or_pull_repo(repo_url, local_path, branch="main"):
    if not os.path.exists(local_path):
        repo = Repo.clone_from(repo_url, local_path, branch=branch)
    else:
        repo = Repo(local_path)
        repo.remotes.origin.pull()
    return repo

