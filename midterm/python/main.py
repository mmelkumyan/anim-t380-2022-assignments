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
import json
import argparse
import copy

import imageio.v3 as iio
from pathlib import Path

"""
Pseudo-code:

- input parameters: frame directory, filters,

- Set frame filter. {scene}_{shot}_{frame# starting at 1000}.{ext}
-- Can filter for scene, shot, frame range, or combo of all 3
- Loop through each image in frames dir
-- Load in with OpenImageIo
-- Check for irregularities. If match, add to bad frames list:
--- file size is vastly different from previous (+- at least 25%?)
--- image is all black, or very close (image value < 5%. from HSV)
- Print contents of bad frames list

"""


def load_naming_convention(naming_json_path: str):
    with open(naming_json_path) as f:
        data = json.load(f)
    return data

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

def filter_images(directory, name_filter):
    # Gather all images in directory
    delimiter = "_"
    images = {}

    for file in Path(frame_dir).iterdir():
        if not file.is_file():
            continue
        # try: # TODO: Try except on invalid named images. Give warning for bad names

        ext = file.suffix
        words = file.stem.split(delimiter)

        if len(words) != len(name_filter):
            print(f"Invalid named file found: {file.name}")
            continue

        for i, (word, range) in enumerate(name_filter.items()):
            num = int(words[i])
            if num < range["min"] or num > range["max"]:
                continue

        images[file.name] = iio.imread(file)
    return images

if __name__ == '__main__':
    naming_words = load_naming_convention("naming.json")

    parser = argparse.ArgumentParser(
        description="This tool helps identify broken frames.")
    parser.add_argument("frames_dir", help="Directory of frames", type=str)
    for word in naming_words["naming"]:
        parser.add_argument(f"--{word}", help="...", type=str)
    args = parser.parse_args()

    frame_dir = args.frames_dir
    raw_filter = vars(args).copy()
    raw_filter.pop("frames_dir")

    name_filter = get_filter_ranges(raw_filter)

    filtered_images = filter_images(args.frames_dir, name_filter)
    x=0

# regex groupdicts in python docs