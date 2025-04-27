import os
import shutil
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Replace with your GitHub token
GITHUB_TOKEN = "ghp_your_personal_access_token_here"
# Insert your real GitHub token into the script.
# --- Repo Configurations ---
REPOS = {
    "repo1": "git@github.com:your-org/repo1.git",
    "repo2": "git@github.com:your-org/repo2.git",
}

# --- Core Logic ---
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

#-- Make sure each repo has a workflow_dispatch-enabled workflow file (.github/workflows/deploy.yml)

def trigger_workflow(repo_name, env_name):
    owner = "your-org"  #--- replace with your organisation value
    repo = repo_name   # -- replace with your repo name 
    workflow_file = "deploy.yml"  # Change if your workflow file is named differently

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "ref": "main",  # Or 'master' or any branch name
        "inputs": {
            "environment": env_name
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print("✅ Workflow triggered successfully.")
    else:
        raise Exception(f"❌ Failed to trigger workflow: {response.status_code} - {response.text}")


# --def deploy(repo_name, env_name):
    #try:
     #   repo_path = clone_or_pull_repo(repo_name)
      #  update_input_yaml(repo_path, env_name)
       # commit_and_push(repo_path, env_name)
        # messagebox.showinfo("Success", f"{repo_name} deployed for {env_name} environment!")
    #except Exception as e:
     #   messagebox.showerror("Error", str(e))

def deploy(repo_name, env_name):
    try:
        repo_path = clone_or_pull_repo(repo_name)
        update_input_yaml(repo_path, env_name)
        commit_and_push(repo_path, env_name)
        trigger_workflow(repo_name, env_name)
        messagebox.showinfo("Success", f"{repo_name} deployed for {env_name} and workflow triggered!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# --- GUI ---
def run_gui():
    root = tk.Tk()
    root.title("Git Deploy GUI")
    root.geometry("400x200")

    tk.Label(root, text="Select Repository").pack(pady=5)
    repo_var = tk.StringVar()
    repo_dropdown = ttk.Combobox(root, textvariable=repo_var, values=list(REPOS.keys()))
    repo_dropdown.pack(pady=5)

    tk.Label(root, text="Select Environment").pack(pady=5)
    env_var = tk.StringVar()
    env_dropdown = ttk.Combobox(root, textvariable=env_var, values=["dev", "staging", "prod"])
    env_dropdown.pack(pady=5)

    def on_deploy():
        repo = repo_var.get()
        env = env_var.get()
        if not repo or not env:
            messagebox.showwarning("Missing Info", "Please select both repo and environment.")
            return
        deploy(repo, env)

    tk.Button(root, text="Deploy", command=on_deploy, bg="green", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
