"""Use a pool of workers to generate thumbnail images.

The `multiprocessing.Pool` class represents a pool of worker processes. It provides an abstraction to split the tasks across processes.

Usage:
    $ python pool_of_workers_thumbnail_generation.py

See Also:
    message_passing_with_pipe.py
    message_passing_with_queue.py
    multiprocess_thumbnail_generation.py
"""
import os
import time
import multiprocessing
import argparse
from argparse import RawDescriptionHelpFormatter
from PIL import Image
from glob import glob


def create_thumbnail(image_file):
    size = 128, 128
    file_name, ext = os.path.splitext(image_file)
    image = Image.open(image_file)
    image.thumbnail(size)
    t_file = f"{file_name}.t.png"
    image.save(t_file, "png")
    process_name = multiprocessing.current_process().name
    img_name = os.path.basename(image_file)
    thumb_name = os.path.basename(t_file)
    print(f"{process_name}: Thumbnail created for {img_name} as {thumb_name}")


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    processor_count = multiprocessing.cpu_count()
    print(f"Detected {processor_count} CPU cores")

    image_dir = os.path.join(os.getcwd(), "data")
    image_files = glob(f"{image_dir}/*.png")

    start = time.time()
    pool = multiprocessing.Pool(processes=processor_count)
    result = pool.map(func=create_thumbnail, iterable=image_files)
    pool.close()
    end = time.time()
    print(f"Total time for thumbnail generation: {(end - start):.2f} seconds")

    # cleanup
    thumbnail_files = glob(f"{image_dir}/*.t.png")
    for path in thumbnail_files:
        print(f"REMOVE {path}")
        os.unlink(path)
