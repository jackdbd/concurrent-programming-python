"""Inter Process Communication (IPC) implemented as message passing between a Producer and a Consumer with a Queue.

A PRODUCER process produces some data and PUTS it in a queue.
A CONSUMER process GETS the data from the queue and produces the output.

Queues are thread and process safe.

Usage:
    $ python message_passing_with_queue.py
"""
import time
import random
import multiprocessing
import argparse
from argparse import RawDescriptionHelpFormatter


class Producer(multiprocessing.Process):

    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        for i in range(10):
            time.sleep(random.random())
            x, y = random.randint(1, 100000), random.randint(1, 100000)
            self.queue.put((x, y))
            print(f"Process {self.name} produced ({x}, {y}) and put it in the queue")


class Consumer(multiprocessing.Process):

    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        # not sure why we have to wait a few ms
        time.sleep(2)
        while not self.queue.empty():
            time.sleep(random.random())
            x, y = self.queue.get()
            print(
                f"Process {self.name} got ({x}, {y}) from the queue and produced {x*y}"
            )

        self.queue.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    queue = multiprocessing.Queue()
    p = Producer(queue)
    c = Consumer(queue)

    p.start()
    c.start()

    p.join()
    c.join()
