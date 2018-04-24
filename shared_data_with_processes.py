"""Example of a shared variable between processes.

Processes do not share the same memory space, so we need special techniques to define shared data and share state across processes.

When doing concurrent programming it is usually best to avoid using shared state as far as possible.
This is particularly true when using multiple processes.
However, if you really do need to use some shared data then `multiprocessing` provides a couple of ways of doing so.
Data can be stored in a shared memory map using `Value` or `Array`.

Usage:
    $ python shared_data_with_processes.py

See Also:
    shared_data_with_threads.py
"""
import argparse
from argparse import RawDescriptionHelpFormatter
from multiprocessing import Process, Array


def target(number, arr):
    print(f"Appending {number}")
    # multiprocessing.Array does not have an append method, so we have to use this
    # syntax (in fact the Array has already 10 elements, so we just have to assign them here)
    arr[number] = number


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    shared_variable = Array(typecode_or_type="i", size_or_initializer=10)

    processes = []
    for i in range(10):
        process_name = f"Subprocess-{i}"
        proc = Process(target=target, args=(i, shared_variable), name=process_name)
        processes.append(proc)

    print(f"State of the shared variable BEFORE processing:")
    for item in shared_variable:
        print(item)
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    print(f"State of the shared variable AFTER processing:")
    for item in shared_variable:
        print(item)
