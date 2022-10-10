from infra.pubsub.pub import ParseMsgPublisher


class WebhookInteractor:
    def __init__(self, publisher: ParseMsgPublisher) -> None:
        self.publisher = publisher

    async def execute_process_gh_push_hook(self, payload) -> None:
        try:
            # Payload: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#push
            repo_fullname = payload["repository"]["full_name"]
            await self.publisher.publish_parse_msg(repo_fullname, "github")
        except Exception as e:
            raise e
