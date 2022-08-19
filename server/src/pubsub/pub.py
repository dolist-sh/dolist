from pubsub.sqs import parse_queue, failed_hook_queue

from storage.mrepodb import read_monitored_repo_by_fullname
from storage.userdb import read_user

from logger import logger

import json


async def publish_parse_msg(repo_fullname: str, provider: str) -> None:
    try:
        repo = await read_monitored_repo_by_fullname(repo_fullname, provider)
        user = await read_user(repo.userId)

        msg = json.dumps(
            dict(
                mrepoId=str(repo.id),
                # userId=str(repo.userId), TODO: Likely not needed, remove this
                token=user.oauth[0]["token"],
                repoName=repo.fullName,
                branch=repo.defaultBranch,  # IDEA: this can take a distinct branch later
                provider=repo.provider,
            ),
        )
        parse_queue.send_message(MessageBody=msg)
    except Exception as e:
        logger.critical(
            f"Publish parse message failed | repo fullname: {repo_fullname}"
        )
        failed_hook_queue.send_message(
            MessageBody=json.dumps(dict(repoName=repo_fullname, provider=provider))
        )
        raise e
