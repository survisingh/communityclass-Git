import os
import subprocess
import sys

def create_virtual_env(env_name="env"):
    """
    Creates a virtual environment if it doesn't exist.
    """
    if not os.path.exists(env_name):
        print(f"Creating virtual environment '{env_name}'...")
        subprocess.check_call([sys.executable, "-m", "venv", env_name])
        print(f"Virtual environment '{env_name}' created.")
    else:
        print(f"Virtual environment '{env_name}' already exists.")

def activate_virtual_env(env_name="env"):
    """
    Activates the virtual environment.
    """
    activate_script = os.path.join(env_name, "Scripts", "activate") if os.name == "nt" else os.path.join(env_name, "bin", "activate")
    print(f"To activate the virtual environment, run:\nsource {activate_script}")

if __name__ == "__main__":
    # Create and prepare the virtual environment
    create_virtual_env()
    activate_virtual_env()
