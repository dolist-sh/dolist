from pubsub.sub import consume_parse_queue, consume_parse_complete_queue
from threading import Timer
import asyncio

# Global variables to track the status of worker
is_parse_worker_busy = False
is_parse_complete_worker_busy = False


def run_parse():
    print("Running worker process for Parse queue..👷‍♂️ 👷‍♂️ ")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    global is_parse_worker_busy

    if is_parse_worker_busy == True:
        print("Parse queue worker is currently processing a message.. 🚧 🚧 🔨 🔨")

    if is_parse_worker_busy == False:
        print("Parse queue worker is not busy, polling a new message.. 🔍 🔍")
        loop.run_until_complete(consume_parse_queue())
        loop.close()

    Timer(30, run_parse).start()


def run_parse_complete():
    print("Running worker process for ParseComplete queue..👷‍♂️ 👷‍♂️")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    global is_parse_complete_worker_busy

    if is_parse_complete_worker_busy == True:
        print("ParseComplete queue worker is currently processing a message.. 🚧 🚧 🔨 🔨")

    if is_parse_worker_busy == False:
        print("ParseComplete queue worker is not busy, polling a new message.. 🔍 🔍")
        loop.run_until_complete(consume_parse_complete_queue())
        loop.close()

    Timer(30, run_parse_complete).start()


if __name__ == "__main__":
    run_parse()
    run_parse_complete()
