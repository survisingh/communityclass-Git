import os
import shutil
import subprocess
from pathlib import Path

REPOS = {
    "repo1": "git@github.com:your-org/repo1.git",
    "repo2": "git@github.com:your-org/repo2.git",
}

def clone_or_pull_repo(repo_name):
    repo_path = Path("repos") / repo_name
    if repo_path.exists():
        subprocess.run(["git", "pull"], cwd=repo_path)
    else:
        subprocess.run(["git", "clone", REPOS[repo_name], str(repo_path)])
    return repo_path

def update_input_yaml(repo_path, env_name):
    src_yaml = Path("env-configs") / f"{env_name}.yaml"
    dest_yaml = repo_path / "conf" / "input.yaml"
    shutil.copy(src_yaml, dest_yaml)

def commit_and_push(repo_path, env_name):
    subprocess.run(["git", "add", "conf/input.yaml"], cwd=repo_path)
    subprocess.run(["git", "commit", "-m", f"Update input.yaml for {env_name}"], cwd=repo_path)
    subprocess.run(["git", "push"], cwd=repo_path)

def deploy(repo_name, env_name):
    repo_path = clone_or_pull_repo(repo_name)
    update_input_yaml(repo_path, env_name)
    commit_and_push(repo_path, env_name)

if __name__ == "__main__":
    import sys
    repo = input("Enter repository name (repo1/repo2): ")
    env = input("Enter environment (dev/staging/prod): ")
    deploy(repo, env)
