import os
import sys

import requests


HOST = os.environ["DATABRICKS_HOST"].rstrip("/")

TOKEN = os.environ["DATABRICKS_TOKEN"]

NOTEBOOK_PATH = os.environ.get(
    "DATABRICKS_NOTEBOOK_PATH",
    "/Shared/github-cicd/main"
)

LOCAL_NOTEBOOK = "notebooks/main.py"


def deploy_notebook():

    print("===================================")
    print("Deploying Databricks notebook")
    print("===================================")

    print(f"Target: {NOTEBOOK_PATH}")

    with open(LOCAL_NOTEBOOK, "r", encoding="utf-8") as file:

        source_code = file.read()


    url = f"{HOST}/api/2.0/workspace/import"


    headers = {

        "Authorization": f"Bearer {TOKEN}"

    }


    payload = {

        "path": NOTEBOOK_PATH,

        "format": "SOURCE",

        "language": "PYTHON",

        "overwrite": True,

        "content": __import__("base64").b64encode(
            source_code.encode("utf-8")
        ).decode("utf-8")

    }


    response = requests.post(

        url,

        headers=headers,

        json=payload,

        timeout=60

    )


    if response.status_code != 200:

        print("Notebook deployment failed.")

        print(response.status_code)

        print(response.text)

        sys.exit(1)


    print("Notebook deployed successfully.")


if __name__ == "__main__":

    deploy_notebook()
