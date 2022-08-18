from pubsub.sub import consume_parse_queue, consume_parse_complete_queue
from helpers.auth import get_auth_token

from core.definition import MachineToken
from threading import Timer
import asyncio, time


# Global variable for machine-to-machine authentication token
token: MachineToken = None


def run_parse():
    print("Running worker process for Parse queue..👷‍♂️ 👷‍♂️ ")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(consume_parse_queue())

    Timer(30, run_parse).start()

    loop.close()


def run_parse_complete():
    print("Running worker process for ParseComplete queue..👷‍♂️ 👷‍♂️")

    global token

    if token == None:
        print(
            "Authentication token is null, can't start pooling the ParseComplete queue.."
        )
        Timer(30, run_parse_complete).start()

    if token != None:
        print(
            "Authentication token found, start pooling a message from the ParseComeplete queue.. 🚧 🚧 🔨 🔨"
        )

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(consume_parse_complete_queue(token))

        Timer(30, run_parse_complete).start()

        loop.close()


if __name__ == "__main__":
    print("Worker has initialized, waiting 10 seconds for server to get up and running")
    time.sleep(10)

    print("Requesting m-to-m auth token")
    token = get_auth_token()

    run_parse()
    run_parse_complete()
