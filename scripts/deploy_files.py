import base64
import os
import sys

import requests


HOST = os.environ["DATABRICKS_HOST"].rstrip("/")
TOKEN = os.environ["DATABRICKS_TOKEN"]

BASE_PATH = "/Workspace/Shared/github-cicd"


FILES = {
    "src/__init__.py": f"{BASE_PATH}/src/__init__.py",
    "src/transformations.py": f"{BASE_PATH}/src/transformations.py",
    "notebooks/main.py": f"{BASE_PATH}/main.py",
}


def get_headers():
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }


def create_directory(path):
    print(f"Creating/checking directory: {path}")

    url = f"{HOST}/api/2.0/workspace/mkdirs"

    response = requests.post(
        url,
        headers=get_headers(),
        json={"path": path},
        timeout=60,
    )

    if response.status_code not in (200, 201):
        print(f"Failed to create directory: {path}")
        print(response.status_code)
        print(response.text)
        sys.exit(1)

    print(f"Directory ready: {path}")


def upload_file(local_path, remote_path):
    print(f"Deploying: {local_path}")
    print(f"Target: {remote_path}")

    with open(local_path, "rb") as file:
        content = base64.b64encode(
            file.read()
        ).decode("utf-8")

    url = f"{HOST}/api/2.0/workspace/import"

    payload = {
        "path": remote_path,
        "format": "SOURCE",
        "language": "PYTHON",
        "overwrite": True,
        "content": content,
    }

    response = requests.post(
        url,
        headers=get_headers(),
        json=payload,
        timeout=60,
    )

    if response.status_code != 200:
        print(f"Failed to deploy: {local_path}")
        print(response.status_code)
        print(response.text)
        sys.exit(1)

    print(f"Successfully deployed: {remote_path}")


def main():
    print("======================================")
    print("Databricks Deployment")
    print("======================================")

    create_directory(BASE_PATH)
    create_directory(f"{BASE_PATH}/src")

    for local_path, remote_path in FILES.items():
        upload_file(local_path, remote_path)

    print("======================================")
    print("Deployment completed successfully")
    print("======================================")


if __name__ == "__main__":
    main()
