from pubsub.sub import consume_parse_queue
from threading import Timer

is_worker_busy = False  # Global variable to track the status of worker


def run_process():
    print("Running worker process..👷‍♂️ 👷‍♂️ ")
    global is_worker_busy

    if is_worker_busy == True:
        print("Worker is currently processing a message.. 🚧 🚧 🔨 🔨")

    if is_worker_busy == False:
        print("Worker is not busy, polling a queue.. 🔍 🔍")
        consume_parse_queue()

    Timer(10, run_process).start()


if __name__ == "__main__":
    run_process()
