import base64
import os
import sys

import requests


HOST = os.environ["DATABRICKS_HOST"].rstrip("/")

TOKEN = os.environ["DATABRICKS_TOKEN"]


FILES = {

    "src/__init__.py":
        "/Shared/github-cicd/src/__init__.py",

    "src/transformations.py":
        "/Shared/github-cicd/src/transformations.py",

    "notebooks/main.py":
        "/Shared/github-cicd/main.py",

}


def upload_file(local_path, remote_path):

    print(f"Deploying {local_path}")

    with open(local_path, "rb") as file:

        content = base64.b64encode(
            file.read()
        ).decode("utf-8")


    url = f"{HOST}/api/2.0/workspace/import"


    headers = {

        "Authorization": f"Bearer {TOKEN}"

    }


    payload = {

        "path": remote_path,

        "format": "SOURCE",

        "language": "PYTHON",

        "overwrite": True,

        "content": content

    }


    response = requests.post(

        url,

        headers=headers,

        json=payload,

        timeout=60

    )


    if response.status_code != 200:

        print(
            f"Failed to deploy {local_path}"
        )

        print(response.text)

        sys.exit(1)


    print(
        f"Successfully deployed {local_path}"
    )


def main():

    for local_path, remote_path in FILES.items():

        upload_file(
            local_path,
            remote_path
        )


if __name__ == "__main__":

    main()
