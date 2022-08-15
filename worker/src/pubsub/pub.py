from pubsub.sqs import parse_complete_queue
from core.definition import ParseCompleteMsg
from typing_extensions import Literal
import ast

# TODO: Add test for this
def publish_result(payload: ParseCompleteMsg) -> Literal["success", "failed"]:
    try:
        msg_body = str(payload)
        result = parse_complete_queue.send_message(MessageBody=msg_body)
        converted = ast.literal_eval(str(result))

        response_code = converted["ResponseMetadata"]["HTTPStatusCode"]

        if response_code == 200:
            return "success"
        else:
            return "failed"
    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e
