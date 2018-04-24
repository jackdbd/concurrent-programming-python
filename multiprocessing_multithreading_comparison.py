"""Comparison between a multi-thread application and a multi-process application.

`multiprocessing` is a package that supports spawning processes using an API similar to the threading module.
With `multiprocessing` we can side-step the Global Interpreter Lock by using subprocesses instead of threads.

When we use multiple processes, we can see that the PID is different.

When we use multiple threads, we can see that the PID does not change.
We are not spawning any new processes, so with multiple threads the PID is the one of the `MainProcess`.

Usage:
    $ python multiprocessing_multithreading_comparison.py 2
"""
import time
import argparse
from argparse import RawDescriptionHelpFormatter
from multiprocessing import Process, current_process
from threading import Thread


def calculate_factorial(number):
    print(f"{current_process().name} (PID:{current_process().pid})")
    fact = 1
    for i in range(1, number):
        fact *= i
    return fact


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "num_processes",
        type=int,
        choices=[1, 2, 3, 4],
        help="Number of processes to spawn and use",
    )
    return parser.parse_args()


if __name__ == "__main__":
    num = 50000
    args = parse_args()

    processes = []
    start = time.time()
    for i in range(args.num_processes):
        process_name = f"Subprocess {i}"
        proc = Process(target=calculate_factorial, args=(num,), name=process_name)
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    end = time.time()
    print(
        f"Processes: It took {(end - start):.2f} seconds with {args.num_processes} subprocesses"
    )

    threads = []
    start = time.time()
    for i in range(args.num_processes):
        thread_name = f"Thread {i}"
        thread = Thread(target=calculate_factorial, args=(num,), name=thread_name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()
    print(
        f"Threads: It took {(end - start):.2f} seconds with {args.num_processes} threads"
    )
