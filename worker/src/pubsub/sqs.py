import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY

sqs = boto3.resource(
    "sqs",
    region_name="eu-west-3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

parse_queue = sqs.get_queue_by_name(QueueName="Parse")
parse_complete_queue = sqs.get_queue_by_name(QueueName="ParseComplete")

# TODO: Create queue if it doesn't exists
