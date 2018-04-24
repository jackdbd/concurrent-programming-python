"""Use of threads with and without a synchronization primitive (Lock).

When NO SYNCHRONIZATION primitive is used, threads might not have enough time to run.
In this example, we might see that the line break of one thread is skipped, because the next threads starts running.
The threads access the console at the same time, so the output is "corrupted".
Try running this script a few times to catch this undesidered behavior.

When a SYNCHRONIZATION primitive is used (e.g. Lock), a thread have always enough time to produce the desired output because the resource (in this case the console, so standard out) is locked.
Try running this script a few times with --lock. You should never see a skipped linebreak.

Usage:
    # without lock (sometimes produces undesidered output)
    $ python threads_with_and_without_lock.py
    # with lock (always produces desidered output)
    $ python threads_with_and_without_lock.py -l
"""
import time
import random
import argparse
from argparse import RawDescriptionHelpFormatter
from threading import Thread, Lock


class URLDownload(Thread):

    def __init__(self, url_name, url, lock=None):
        Thread.__init__(self)
        self.url = url
        self.url_name = url_name
        self.lock = lock

    def run(self):
        time.sleep(random.random())
        if self.lock is not None:
            self.lock.acquire()
            print(f"{self.name} (LOCK): URL: {self.url}, URLName: {self.url_name}\n")
            self.lock.release()
        else:
            print(f"{self.name}: URL: {self.url}, URLName: {self.url_name}\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-l",
        "--lock",
        action="store_true",
        help="Use a synchronization primitive for the threads (Lock)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    threads = []
    test_dict = {
        "Google": "http://www.google.com",
        "Python": "http://www.python.org",
        "Bing": "http://www.bing.com",
        "Yahoo": "http://www.yahoo.com",
        "Amazon": "http://www.amazon.com",
        "Nike": "http://www.nike.com",
        "Wikipedia": "https://www.wikipedia.com",
    }
    if args.lock:
        print_lock = Lock()

    for key in test_dict:
        for i in range(10):
            if args.lock:
                thread = URLDownload(key, test_dict[key], lock=print_lock)
            else:
                thread = URLDownload(key, test_dict[key])
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
