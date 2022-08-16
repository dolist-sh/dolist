from pubsub.sqs import parse_queue
from pubsub.pub import publish_result

from core.github import parse_github_repo
from core.definition import ParseRequestMsg, ParseCompleteMsg

from config import JWT_SECRET
from helpers.logger import logger
import json, jwt


async def consume_parse_queue():
    global is_worker_busy

    try:
        for msg in parse_queue.receive_messages(MaxNumberOfMessages=1):
            print("Received a message from Parse queue")
            print("------------------")
            print(f"Message body: ${msg.body}")
            print("------------------")

            is_worker_busy = True

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

            is_worker_busy = False

    except Exception as e:
        is_worker_busy = False
        logger.critical(f"Unexpected issuewhile attemping to process the message: {str(e)}")
