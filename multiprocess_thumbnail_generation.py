"""Use multiple processes to generate thumbnail images.

Manually split the work across processes, to maximize the use of all CPU cores.

Usage:
    $ python multiprocess_thumbnail_generation.py

See Also:
    message_passing_with_pipe.py
    message_passing_with_queue.py
    pool_of_workers_thumbnail_generation.py
"""
import os
import time
import multiprocessing
import argparse
from argparse import RawDescriptionHelpFormatter
from PIL import Image
from glob import glob


def create_thumbnail(image_files):
    size = 128, 128
    for image_file in image_files:
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

    # manually split the work across CPU cores
    images_per_process = (int)(len(image_files) / processor_count) + 1
    print(
        f"{len(image_files)} images. Split work: {images_per_process} images per process"
    )

    processes = []
    start = time.time()
    for i in range(processor_count):
        if (i + 1) * images_per_process > len(image_files):
            image_file_subset = image_files[i * images_per_process:]
        else:
            image_file_subset = image_files[
                i * images_per_process:(i + 1) * images_per_process
            ]

        p = multiprocessing.Process(target=create_thumbnail, args=(image_file_subset,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = time.time()
    print(f"Total time for thumbnail generation: {(end - start):.2f} seconds")

    # cleanup
    thumbnail_files = glob(f"{image_dir}/*.t.png")
    for path in thumbnail_files:
        print(f"REMOVE {path}")
        os.unlink(path)
