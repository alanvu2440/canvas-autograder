import os
import shutil
from git import Repo

def clone_repo(url, repo_dir):
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    Repo.clone_from(url, repo_dir)