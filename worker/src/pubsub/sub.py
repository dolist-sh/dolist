from pubsub.sqs import parse_queue, parse_complete_queue
from pubsub.pub import publish_result

from core.github import parse_github_repo
from core.definition import ParseRequestMsg, ParseCompleteMsg, MachineToken

from config import JWT_SECRET, SERVER_HOST
from helpers.logger import logger
import json, jwt, requests


async def consume_parse_queue() -> None:
    try:
        for msg in parse_queue.receive_messages(MaxNumberOfMessages=1):
            print("Received a message from Parse queue")
            print("------------------")
            print(f"Message body: ${msg.body}")
            print("------------------")

            data: ParseRequestMsg = json.loads(msg.body)

            userId = data["userId"]
            token = data["token"]
            repo_name = data["repoName"]
            branch = data["branch"]
            provider = data["provider"]

            # TODO: Add provider check when more integration are in place
            parse_output = parse_github_repo(token, repo_name, branch)

            print("------------------")
            print("Parse output: ")
            print(parse_output)
            print("------------------")

            encode_payload = {"result": parse_output}
            encoded = jwt.encode(encode_payload, JWT_SECRET, algorithm="HS256")

            print("------------------")
            print("Encoded output: ")
            print(encoded)
            print("------------------")

            msg_payload: ParseCompleteMsg = dict(
                userId=userId,
                repoName=repo_name,
                branch=branch,
                provider=provider,
                hashedResult=encoded,
            )

            pub_result = await publish_result(msg_payload)

            if pub_result == "success":
                logger.info(f"Parsing complete for message: ${msg.body}")
                msg.delete()

    except Exception as e:
        logger.critical(
            f"Unexpected issuewhile attemping to process the message from Parse queue: {str(e)}"
        )


async def consume_parse_complete_queue(token: MachineToken) -> None:
    try:
        for msg in parse_complete_queue.receive_messages(MaxNumberOfMessages=1):
            print("Received a message from ParseComplete queue")
            print("------------------")
            print(f"Message body: ${msg.body}")
            print("------------------")

            headers = {
                "Accept": "application/json",
                "Authorization": f"token {token['access_token']}",
            }
            host = f"{SERVER_HOST}/parse/result"

            #payload = json.dumps(json.loads(msg.body))
            #print(payload)

            dummy = {
                "example": "example"
            }

            res = requests.post(host, headers=headers, data=json.dumps(dummy))

            if res.status_code == 201:
                logger.info(f"Parsing result has been processed | original message: {msg.body}")
                msg.delete()

            return
    except Exception as e:
        logger.critical(
            f"Unexpected issue while attemping to process the message from ParseComplete queue: {str(e)}"
        )
