from infra.storage.mrepodb import MonitoredRepoDBAccess
from infra.storage.userdb import UserDBAccess
from logging import Logger


class ParseMsgPublisher:
    def __init__(
        self,
        parse_queue,
        failed_msg_queue,
        mrepodb: MonitoredRepoDBAccess,
        userdb: UserDBAccess,
        logger: Logger,
    ) -> None:
        """
        Type definition of queues:
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html?highlight=sqs#queue
        """
        self.parse_queue = parse_queue
        self.failed_msg_queue = failed_msg_queue
        self.mrepodb = mrepodb
        self.userdb = userdb
        self.logger = logger

    async def publish_parse_msg(self, repo_fullname: str, provider: str) -> None:
        import json

        try:
            repo = await self.mrepodb.read_monitored_repo_by_fullname(
                repo_fullname, provider
            )
            user = await self.userdb.read_user(repo.userId)

            msg = json.dumps(
                dict(
                    mrepoId=str(repo.id),
                    token=user.oauth[0]["token"],
                    repoName=repo.fullName,
                    branch=repo.defaultBranch,  # IDEA: this can take a distinct branch later
                    provider=repo.provider,
                ),
            )
            self.parse_queue.send_message(MessageBody=msg)
        except Exception as e:
            self.logger.critical(
                f"Publish parse message failed | repo fullname: {repo_fullname}"
            )
            self.failed_msg_queue.send_message(
                MessageBody=json.dumps(dict(repoName=repo_fullname, provider=provider))
            )
            raise e
