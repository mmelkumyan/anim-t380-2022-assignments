"""
Problem 3
Overview:
The compositing supervisor is requesting a tool to help identify broken frames.
Create a utility that:

- collects a sequence of frames based on a naming convention
- identifies frames either vastly different in filesize or are completely black
- generates a report that lists potential frames to be reviewed (text, html, or email)
- Extra credit feature: combine thumbnails in a single grid image for quick reference

Hints:
Use a well-defined naming convention similar to one discussed in the lecture.
To identify a frame that is completely black, a python approach that is worth looking
at is OpenImageIO. You could do it with ffmpeg, but it would be trickier.
"""
import argparse
import os

import imageio.v3 as iio
from pathlib import Path


# Pseudo-code:
#
# - input parameters: frame directory, filters,
#
# - Set frame filter. {scene}_{shot}_{frame# starting at 1000}.{ext}
# -- Can filter for scene, shot, frame range, or combo of all 3
# - Loop through each image in frames dir
# -- Load in with OpenImageIo
# -- Check for irregularities. If match, add to bad frames list:
# --- file size is vastly different from previous (+- at least 25%?)
# --- image is all black, or very close (image value < 5%. from HSV)
# - Print contents of bad frames list

NAMING_CONVENTION_TXT = "./naming.txt"

def load_naming_convention(naming_txt_path: str):
    with open(naming_txt_path) as f:
        line = f.readline()
    file_name, ext = line.split(".")
    name_words = file_name.split("_")
    return  name_words, ext


def get_filter_ranges(raw_filter):
    clean_filter = {}
    for key, value in raw_filter.items():
        nums = value.split("-")

        range = {
            "min": -1,
            "max": -1
        }
        num_cnt = len(nums)
        if num_cnt == 1:
            num = int(nums[0])
            range["min"] = num
            range["max"] = num
        elif num_cnt == 2:
            range["min"] = int(nums[0])
            range["max"] = int(nums[1])
        else:
            raise ValueError(f"Invalid {key} range: {value}")

        clean_filter[key] = range

    return clean_filter


def gather_images_info(directory: str, name_filter: dict, ext_filter: str):
    # Gather all images in directory
    images_info = {}

    for file in Path(directory).iterdir():
        # Skip over directories
        if not file.is_file():
            continue

        # Filter file extensions
        if not file.match(f'*.{ext_filter}'):
            continue

        # TODO: try regex for matching!

        # Get words from file name
        file_name_words = file.stem.split("_")

        # Ensure number of file name words is expected
        if len(file_name_words) != len(name_filter):
            print(f"Invalid named file found. Incorrect number of words: {file.name}")
            continue

        # Filter number ranges on file name
        for i, num_range in enumerate(name_filter.values()):
            # Ensure word is integer
            try:
                word_num = int(file_name_words[i])
            except ValueError:
                print(f"Invalid named file found. "
                      f"Non-integer found: {file_name_words[i]} in {file.name}")
                continue

            # Filter integers out of range
            if word_num < num_range["min"] or word_num > num_range["max"]:
                continue

        # Create dictionary to hold image info
        images_info[file.name] = {}
        # Read in image
        images_info[file.name]["image"] = iio.imread(file)
        # Record file size
        images_info[file.name]["size"] = file.stat().st_size
    return images_info


if __name__ == '__main__':
    naming_words, ext = load_naming_convention(NAMING_CONVENTION_TXT)

    parser = argparse.ArgumentParser(
        description="This tool helps identify broken frames.")
    parser.add_argument("frames_dir", help="Directory of frames", type=str)
    for word in naming_words:
        parser.add_argument(f"--{word}", help="...", type=str)
    args = parser.parse_args()

    frame_dir = args.frames_dir
    raw_filter = vars(args).copy()
    raw_filter.pop("frames_dir")

    name_filter = get_filter_ranges(raw_filter)

    images = gather_images_info(args.frames_dir, name_filter, ext)


    x=0
# regex groupdicts in python docs
