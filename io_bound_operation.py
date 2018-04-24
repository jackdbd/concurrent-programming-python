"""Example of a IO bound operation.

Usage:
    $ python io_bound_operation.py
"""
import time
import urllib.request
import argparse
from argparse import RawDescriptionHelpFormatter
from threading import Thread, current_thread


def download_file(url):
    urllib.request.urlretrieve(url, "7zip{}.zip".format(str(current_thread().name)))


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
    url = "http://www.7-zip.org/a/7z1701.msi"
    args = parse_args()

    start = time.time()
    threads = []
    for _ in range(args.num_threads):
        t = Thread(target=download_file, args=(url,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

    end = time.time()
    print(f"Processing with {args.num_threads} threads took {(end - start):.2f} seconds")
