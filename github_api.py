import requests
import os

TOKEN = os.getenv("GITHUB_TOKEN")


def comment_pr(repo, pr, body):

    url = f"https://api.github.com/repos/{repo}/issues/{pr}/comments"

    headers = {
        "Authorization": f"token {TOKEN}"
    }

    requests.post(url, headers=headers, json={"body": body})