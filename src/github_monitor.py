import os
from git import Repo
import shutil
import uuid
import os
def clone_or_pull_repo(repo_url, base_path):
    repo_name = repo_url.rstrip("/").split("/")[-1]
    scan_id = str(uuid.uuid4())[:8]

    repo_path = os.path.join(base_path, f"{repo_name}_{scan_id}")
    os.makedirs(base_path, exist_ok=True)

    repo = Repo.clone_from(repo_url, repo_path)
    return repo

