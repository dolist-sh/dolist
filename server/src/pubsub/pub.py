from pubsub.sqs import parse_queue

from domain.mrepo import MonitoredRepo
from typing import List

import json

# TODO: return status and catch exception
def publish_parse_req(payload: List[MonitoredRepo], oauth_token: str):
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
