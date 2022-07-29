import requests
import re
import base64
from dolistparser import js_gh_parser, py_gh_parser, ParsedComment
from typing import List


async def get_github_repos(access_token: str):
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {access_token}",
        }
        host = "https://api.github.com/user/repos"

        res = requests.get(host, headers=headers)

        return res.json()

    except Exception as e:
        raise e


async def parse_github_repo(
    access_token: str, repo_name: str, branch: str
) -> List[ParsedComment]:
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {access_token}",
        }

        # Get the branch detail to find the sha of the latest commit

        host = f"https://api.github.com/repos/{repo_name}/branches/{branch}"
        res_branch = requests.get(host, headers=headers)
        data_branch = res_branch.json()

        # Recursively call the git tree API for full list of source files
        # https://docs.github.com/en/rest/git/trees#get-a-tree

        uri_tree_api = data_branch["commit"]["commit"]["tree"]["url"]
        res_tree = requests.get(f"{uri_tree_api}?recursive=true", headers=headers)
        data_tree = res_tree.json()

        result = []

        for data in data_tree["tree"]:
            # if data['type'] == 'tree':
            # tree type is directory

            if data["type"] == "blob":
                file_path = data["path"]
                blob_url = data["url"]

                # Get the content of the file
                # https://docs.github.com/en/rest/git/blobs#get-a-blob

                blob_res = requests.get(blob_url, headers=headers)
                data_blob = blob_res.json()

                file_content = base64.b64decode(data_blob["content"])
                content_to_parse = str(file_content).split(("\\n"))

                parsed = []

                if re.search(r"(\.js$|\.ts$)", file_path, re.IGNORECASE):
                    parsed = js_gh_parser.parse(content_to_parse, file_path)

                if re.search(r"(\.py$)", file_path, re.IGNORECASE):
                    parsed = py_gh_parser.parse(content_to_parse, file_path)

                result = result + parsed

        return result
    except Exception as e:
        raise e
