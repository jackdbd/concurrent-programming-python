"""Producer - Consumer pattern with a FIFO Queue.

The queue module implements multi-producer, multi-consumer queues.
The Queue class implements a FIFO queue with all locking semantics required.

Usage:
    $ python producer_consumer_queue.py

See Also:
    producer_consumer_pattern.py
"""
import time
import random
import argparse
import threading
import queue
from argparse import RawDescriptionHelpFormatter


NUM_ITEMS = 10

# create a FIFO queue
q = queue.Queue()


class Producer(threading.Thread):

    def run(self):
        for i in range(NUM_ITEMS):
            x, y = random.randint(1, 100000), random.randint(1, 100000)
            q.put((x, y))
            print(f"ITEM {i} added to FIFO queue")
            print(f"{self.name} added: ({x}, {y})")
            time.sleep(random.random())


class Consumer(threading.Thread):

    def run(self):
        for i in range(NUM_ITEMS):
            time.sleep(random.random())
            x, y = q.get()
            print(f"Product of ({x}*{y}) = {x*y}")
            print(f"ITEM {i} processed")
            q.task_done()


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    Producer().start()
    Consumer().start()
    # make sure to lock the main thread until all items in the queue have been processed
    q.join()
