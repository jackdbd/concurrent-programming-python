"""Producer - Consumer pattern.

This script goes on forever. Terminate it with Ctrl+C.

Some producer/s thread/s produce/s some sort of data or item and put it into a SHARED buffer (here is a simple python list).
Producer threads should not put more data than the buffer can contain.

Some consumer/s thread/s fetch/es the data from the buffer.
Consumer thread should not read from an empty buffer.

Usage:
    $ python producer_consumer_pattern.py

See Also:
    producer_consumer_queue.py
"""
import time
import random
import argparse
import threading
from argparse import RawDescriptionHelpFormatter

# we use a list to act as the shared buffer
operands = []

# event used to understand whether the shared buffer is accessible or not
event = threading.Event()


class Producer(threading.Thread):

    def run(self):
        while True:
            (x, y) = random.randint(1, 100000), random.randint(1, 100000)
            operands.append((x, y))
            print(f"{self.name} added: ({x}, {y})")
            # set an event to communicate that the buffer can be read by a consumer thread
            event.set()
            time.sleep(random.random())


class Consumer(threading.Thread):

    def run(self):
        while True:
            time.sleep(random.random())
            # wait for an event to avoid reading from an empty buffer. This event is set by the producer thread
            event.wait()
            (x, y) = operands.pop()
            print(f"Product of ({x}*{y}) = {x*y}")
            # clear the event, so the producer thread can set it again
            event.clear()


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    Producer().start()
    Consumer().start()
