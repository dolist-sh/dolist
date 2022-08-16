from pubsub.sub import consume_parse_queue
from threading import Timer
import asyncio

is_worker_busy = False  # Global variable to track the status of worker

def run():
    print("Running worker process..👷‍♂️ 👷‍♂️ ")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    global is_worker_busy

    if is_worker_busy == True:
        print("Worker is currently processing a message.. 🚧 🚧 🔨 🔨")

    if is_worker_busy == False:
        print("Worker is not busy, polling a queue.. 🔍 🔍")
        loop.run_until_complete(consume_parse_queue())
        loop.close()
    
    Timer(30, run).start()
   

if __name__ == "__main__":
    run()