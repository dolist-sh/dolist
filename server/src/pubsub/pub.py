from pubsub.sqs import parse_queue

from storage.mrepodb import read_monitored_repo_by_fullname
from storage.userdb import read_user

from domain.mrepo import MonitoredRepo
from typing import List

from logger import logger

import json


async def publish_parse_msg(repo_fullname: str, provider: str) -> None:
    try:
        repo = await read_monitored_repo_by_fullname(repo_fullname, provider)
        user = await read_user(repo.userId)
        msg = json.dumps(
            dict(
                userId=str(repo.userId),
                token=user.oauth[0]["token"],
                repoName=repo.fullName,
                branch=repo.defaultBranch,
                provider=repo.provider,
            ),
        )
        parse_queue.send_message(MessageBody=msg)
    except Exception as e:
        # TODO: Send failed webhook to a separate queue
        logger.critical(
            f"Publish parse message failed | repo fullname: {repo_fullname}"
        )
        raise e


async def publish_parse_msg_batch(
    payload: List[MonitoredRepo], oauth_token: str
) -> None:
    try:
        msgs = [
            dict(
                Id=str(mrepo.id),
                MessageBody=json.dumps(
                    dict(
                        userId=str(mrepo.userId),
                        token=oauth_token,
                        repoName=mrepo.fullName,
                        branch=mrepo.defaultBranch,
                        provider=mrepo.provider,
                    ),
                ),
            )
            for mrepo in payload
        ]
        parse_queue.send_messages(Entries=msgs)
    except Exception as e:
        # TODO: Send failed webhook to a separate queue
        logger.critical("Batch parse message failed")
        raise e
