"""Example of a shared variable between threads (not thread safe).

Threads share the same memory space.

Usage:
    $ python shared_data_with_threads.py

See Also:
    shared_data_with_processes.py
"""
import argparse
from argparse import RawDescriptionHelpFormatter
from threading import Thread


def target(number, arr):
    print(f"Appending {number}")
    arr.append(number)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    shared_variable = []

    threads = []
    for i in range(10):
        thread_name = f"Thread-{i}"
        thread = Thread(target=target, args=(i, shared_variable), name=thread_name)
        threads.append(thread)

    print(f"State of the shared variable BEFORE processing: {shared_variable}")
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"State of the shared variable AFTER processing: {shared_variable}")
