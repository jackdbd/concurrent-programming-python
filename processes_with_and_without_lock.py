"""Use of process with and without a synchronization primitive (Lock).

When NO SYNCHRONIZATION primitive is used, two or more processes might access their shared data and modify it at the same time.
This is called "race condition": the output is dependent on the sequence or timing of uncontrollable events.
In this script we increment and decrement an equal number of times, so we expect to find that the shared variable has value 0.
This means that whenever after processing the shared variable is not zero, we encountered a race condition.
Try running this script a few times to catch this undesidered behavior.

When a SYNCHRONIZATION primitive is used (e.g. Lock), we avoid these timing issues, so no race condition is triggered.
Of course the synchronization will increase the running time.

Usage:
    # without lock (sometimes produces undesidered output)
    $ python processes_with_and_without_lock.py
    # with lock (always produces desidered output)
    $ python processes_with_and_without_lock.py -l
"""
import time
import argparse
from argparse import RawDescriptionHelpFormatter
from multiprocessing import Process, Value, Lock


NUM_ITERATIONS = 100000


def increment(num, lock=None):
    for _ in range(NUM_ITERATIONS):
        if lock is not None:
            # instead of manually calling lock.acquire and lock.release, we can use a context manager
            with lock:
                num.value = num.value + 1
        else:
            num.value = num.value + 1


def decrement(num, lock=None):
    for _ in range(NUM_ITERATIONS):
        if lock is not None:
            with lock:
                num.value = num.value - 1
        else:
            num.value = num.value - 1


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l",
        "--lock",
        action="store_true",
        help="Use a synchronization primitive for the processes (Lock)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    num = Value("i", 0)
    print(f"BEFORE processing {num.value}")

    if args.lock:
        lock = Lock()
        p1 = Process(target=increment, args=(num, lock))
        p2 = Process(target=decrement, args=(num, lock))
    else:
        p1 = Process(target=increment, args=(num,))
        p2 = Process(target=decrement, args=(num,))

    start = time.time()
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    end = time.time()

    print(f"AFTER processing {num.value}")
    print(f"{(end-start):.2f} seconds")
