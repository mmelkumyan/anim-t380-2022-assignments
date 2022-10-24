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


def filter_images(directory, name_filter):
    # Gather all images in directory
    delimiter = "_"
    images = {}

    for file in Path(frame_dir).iterdir():
        if not file.is_file():
            continue
        # try: # TODO: Try except on invalid named images. Give warning for bad names
        ext = file.suffix

        scene, shot, frame = file.stem.split(delimiter)
        # file.

        images[file.name] = iio.imread(file)


if __name__ == '__main__':
    naming_words = load_naming_convention("naming.json")

    parser = argparse.ArgumentParser(
        description="This tool helps identify broken frames.")
    parser.add_argument("frames_dir", help="Directory of frames", type=str)
    for word in naming_words["naming"]:
        parser.add_argument(f"--{word}", help="...", type=str)
    args = parser.parse_args()

    frame_dir = args.frames_dir
    name_filter = vars(args).copy()
    name_filter.pop("frames_dir")

    # name_filter = {arg: value for arg, value in vars(args).items() if
    #                arg != "frames_dir"}

    filter_images(args.frames_dir, name_filter)
    x = 0
