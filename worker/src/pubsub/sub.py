from pubsub.sqs import parse_queue

from core.github import parse_github_repo
from core.definition import ParseRequestMsg, MachineToken

from config import SERVER_HOST
from helpers.logger import logger
import json, requests


async def consume_parse_queue(machine_token: MachineToken) -> None:
    try:
        for msg in parse_queue.receive_messages(MaxNumberOfMessages=1):
            print("Received a message from Parse queue")
            print("------------------")
            print(f"Message body: ${msg.body}")
            print("------------------")

            data: ParseRequestMsg = json.loads(msg.body)

            user_id = data["userId"]
            github_oauth_token = data["token"]
            repo_name = data["repoName"]
            branch = data["branch"]
            

            # TODO: Add provider check when more integration are in place
            # provider = data["provider"]
            parse_output = parse_github_repo(github_oauth_token, repo_name, branch)

            print("------------------")
            print("Parse output: ")
            print(parse_output)
            print("------------------")

            headers = {
                "Accept": "application/json",
                "Authorization": f"token {machine_token['access_token']}",
            }
            host = f"{SERVER_HOST}/parse/result"

            payload = {
                "userId":  user_id,
                "repoFullname": repo_name,
                "branch": branch,
                "parseResult": parse_output
                #TODO: add the last commit here
            }

            res = requests.post(host, headers=headers, data=json.dumps(payload))

            if res.status_code == 201:
                logger.info(f"Parsing result has been processed | original message: {msg.body}")
                msg.delete()

    except Exception as e:
        logger.critical(
            f"Unexpected issuewhile attemping to process the message from Parse queue: {str(e)}"
        )
