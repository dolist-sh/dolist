from pubsub.sqs import parse_queue
from pubsub.pub import publish_result

from core.github import parse_github_repo
from core.definition import ParseRequestMsg, ParseCompleteMsg

from config import JWT_SECRET
import json, jwt


def consume_parse_queue():
    try:
        for msg in parse_queue.receive_messages(MaxNumberOfMessages=1):
            print("Received a message from Parse queue")
            print("------------------")
            print(msg.body)
            print("------------------")

            data: ParseRequestMsg = json.loads(msg.body)

            # TODO: Gracefully handle the KeyError due to malformed message body
            userId = data["userId"]
            token = data["token"]
            repo_name = data["repoName"]
            branch = data["branch"]
            provider = data["provider"]

            # TODO: Add provider check when more integration are in place
            result = parse_github_repo(token, repo_name, branch)

            print("------------------")
            print("Parse result: ")
            print(result)
            print("------------------")

            payload = {"result": result}
            encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

            print("------------------")
            print("Encoded result: ")
            print(encoded)
            print("------------------")

            payload: ParseCompleteMsg = dict(
                userId=userId,
                repoName=repo_name,
                branch=branch,
                provider=provider,
                hashedResult=encoded,
            )

            result = publish_result(payload)

            if result == "success":
                msg.delete()

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e
