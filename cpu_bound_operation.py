"""Example of a CPU bound operation.

Usage:
    $ python cpu_bound_operation.py
"""
import time
import argparse
from argparse import RawDescriptionHelpFormatter
from threading import Thread


def calculate_factorial(number):
    factorial = 1
    for n in range(1, number + 1):
        factorial *= n
    return factorial


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "num_threads",
        type=int,
        choices=[1, 2, 3, 4],
        help="Number of threads to spawn and use",
    )
    return parser.parse_args()


if __name__ == "__main__":
    number = 100000
    args = parse_args()

    start = time.time()
    threads = []
    for _ in range(args.num_threads):
        t = Thread(target=calculate_factorial, args=(number,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end = time.time()
    print(f"Processing with {args.num_threads} threads took {(end - start):.2f} seconds")
