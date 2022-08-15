import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY

sqs = boto3.resource(
    "sqs",
    region_name="eu-west-3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

parse_queue = sqs.get_queue_by_name(QueueName="Parse")


def consume_queue():
    for msg in parse_queue.receive_messages(MaxNumberOfMessages=10):
        print("------")
        print(msg)
        print("---")
        print(msg.body)
        print("------")
        msg.delete()
