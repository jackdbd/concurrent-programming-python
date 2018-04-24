"""Inter Process Communication (IPC) implemented as message passing between a Producer and a Consumer through a Pipe.

A PRODUCER process produces some data and SENDS it through a pipe.
A CONSUMER process RECEIVES the data from the pipe and produces the output.

Usage:
    $ python message_passing_with_pipe.py
"""
import random
import multiprocessing
import argparse
from argparse import RawDescriptionHelpFormatter


class Producer(multiprocessing.Process):

    def __init__(self, conn):
        multiprocessing.Process.__init__(self)
        self.conn = conn

    def run(self):
        for i in range(10):
            x, y = random.randint(1, 100000), random.randint(1, 100000)
            self.conn.send((x, y))
            print(
                f"Process {self.name} produced ({x}, {y}) and sent it through the (unidirectional) pipe"
            )
        self.conn.close()


class Consumer(multiprocessing.Process):

    def __init__(self, conn):
        multiprocessing.Process.__init__(self)
        self.conn = conn

    def run(self):
        while True:
            try:
                x, y = self.conn.recv()
                print(f"Process {self.name} consumed ({x}, {y}) and produced {x*y}")
            except EOFError:
                print("No more data to consume...")
                break

        self.conn.close()


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # create a unidirectional pipe, so we have a connection to receive the data and a connection to send the data
    (recv, send) = multiprocessing.Pipe(duplex=False)

    p = Producer(conn=send)
    p.start()
    send.close()

    c = Consumer(conn=recv)
    c.start()
