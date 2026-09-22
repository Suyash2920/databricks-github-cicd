import os
import json
import requests


def analyze_failure():

    api_key = os.environ["AI_API_KEY"]

    logs = ""

    if os.path.exists("test-results.txt"):

        with open(
            "test-results.txt",
            "r",
            encoding="utf-8"
        ) as file:

            logs = file.read()


    prompt = f"""
You are a CI/CD troubleshooting assistant.

Analyze the following pipeline failure.

CI LOG:

{logs}

Provide:

1. Root cause
2. Failed component
3. Recommended fix
4. Additional test recommendation
5. Security concerns
6. Whether human review is required

Do not modify or execute code.
"""


    response = requests.post(

        "https://api.openai.com/v1/responses",

        headers={

            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json"

        },

        json={

            "model": os.environ.get(
                "AI_MODEL",
                "gpt-5"
            ),

            "input": prompt

        },

        timeout=60

    )


    response.raise_for_status()


    result = response.json()


    print(json.dumps(
        result,
        indent=2
    ))


if __name__ == "__main__":

    analyze_failure()
