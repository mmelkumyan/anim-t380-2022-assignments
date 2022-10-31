"""
Broken Frames Analyzer
"""
import argparse
from pathlib import Path
from typing import List

import cv2
import numpy as np

NAMING_CONVENTION_TXT = "./naming.txt"
BYTES_IN_MEGABYTE = 1048576


def load_naming_convention(naming_txt_path: str) -> (List[str], str):
    """
    Loads naming conventions from .txt file.
    Splits naming words with '_' character.

    :param naming_txt_path: Relative path to .txt file.
    :return: tuple containing list of naming words and extension
    """
    # Read file line
    with open(naming_txt_path, encoding="utf-8") as file:
        line = file.readline()
    # Extract name words and extension
    file_name, ext = line.split(".")
    name_words = file_name.split("_")
    return name_words, ext


def get_filter_ranges(raw_filter: dict) -> dict:
    """
    Converts user input filter ranges into dictionary

    :param raw_filter: Dictionary containing filter for each file name word.
        Ex: {'scene': '001', 'frame': '1000-1005'}
    :return: Dictionary containing integer ranges for each file name item.
        Ex: {'scene': {'min': 1, 'max': 1}, 'frame': {'min': 1000, 'max': 1005}}
    """
    clean_filter = {}
    for name_word, range_str in raw_filter.items():
        if not range_str:
            clean_filter[name_word] = None
            continue
        num_strs = range_str.split("-")

        num_range = {}
        cnt = len(num_strs)
        if cnt == 1:
            num_range["min"] = int(num_strs[0])
            num_range["max"] = int(num_strs[0])
        elif cnt == 2:
            num_range["min"] = int(num_strs[0])
            num_range["max"] = int(num_strs[1])
        else:
            raise ValueError(f"Invalid {name_word} range: {range_str}")
        clean_filter[name_word] = num_range

    return clean_filter


def get_images_info(directory: str, name_filter: dict, ext_filter: str) -> dict:
    """
    Filters out desired images in directory and returns dictionary of image info.
    Output dictionary format:
    "<image name>" : {
        "image": numpy image array
        "size": size of image in megabytes
        "warnings": empty list to add warnings to
    }

    :param directory:
    :param name_filter: Dictionary containing number range for each name word
    :param ext_filter: File extension of images
    :return: Dictionary containing information of each image.
    """
    # Gather all images in directory
    images_info = {}

    for file in Path(directory).iterdir():
        # Skip over directories
        if not file.is_file():
            continue

        # Filter file extensions
        if not file.match(f'*.{ext_filter}'):
            continue

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
            if num_range and (
                    word_num < num_range["min"] or word_num > num_range["max"]):
                continue

        # Create dictionary to hold image info
        images_info[file.name] = {}
        # Read in image
        images_info[file.name]["image"] = cv2.imread(str(file))
        # Record file size
        images_info[file.name]["size"] = file.stat().st_size / BYTES_IN_MEGABYTE
        # List to hold image warnings
        images_info[file.name]["warnings"] = []

    return images_info


def find_small_images(images_info: dict, size_threshold_mb: int = .2) -> None:
    """
    Checks each image in images_info to see if file size is below threshold and adds
    warning if so.

    :param images_info: Dictionary containing information of each image
    :param size_threshold_mb: Threshold for image size in megabytes. Images below
        this size are given a warning.
        Default is 0.2 MB.
    """
    for file_name, im_info in images_info.items():
        size = im_info["size"]

        # If below threshold, record warning
        if size <= size_threshold_mb:
            warning = f"Small image - Image size is {size:.6f} megabytes"
            images_info[file_name]["warnings"].append(warning)


def find_black_images(images_info: dict, value_threshold: float = .02) -> None:
    """
    Checks each image in images_info to see if value is below threshold and adds warning
    if so.

    :param images_info: Dictionary containing information of each image
    :param value_threshold: Float from 0-1 threshold for image value. Images with an
        average pixel value below this are given a warning.
        0.0 is a black image, 0.5 is a 50% grey image, and 1.0 is a white image.
        Default is 0.02.
    """
    for file_name, im_info in images_info.items():
        # Convert image to HSV
        hsv_image = cv2.cvtColor(im_info["image"], cv2.COLOR_BGR2HSV)
        # Get average value of image
        avg_value = hsv_image[:, :, 2].mean() / 255

        # If below threshold, record warning
        if avg_value <= value_threshold:
            warning = f"Dark image - Average value of {avg_value * 100:.2f}%"
            images_info[file_name]["warnings"].append(warning)


def print_report(images_info: dict) -> None:
    """
    Outputs warnings of each image to command line.

    :param images_info: Dictionary containing information of each image
    """
    for file_name, im_info in images_info.items():
        # Skip images without warnings
        if not im_info["warnings"]:
            continue

        # Output warnings
        print(file_name)
        for warning in im_info["warnings"]:
            print("\t" + warning)


def create_warning_image_grid(images_info: dict,
                              file_name: str = "warningImageThumbnails.jpg") -> None:
    """
    Outputs a grid of thumbnails of images with warnings to the current directory.

    :param images_info: Dictionary containing information of each image
    :param file_name: Name of the grid image to save
    """
    grid_width = 4  # Number of thumbnails per row
    grid_im_width = 100  # Width of each thumbnail

    # Filter out images with warnings
    warn_images = [v["image"] for k, v in images_info.items() if v["warnings"]]

    # Shrink images down
    im_height, im_width, im_depth = warn_images[0].shape
    grid_im_height = int(grid_im_width * im_height / im_width)
    new_dims = grid_im_width, grid_im_height
    grid_images = [cv2.resize(im, new_dims, interpolation=cv2.INTER_LINEAR)
                   for im in warn_images]

    # Add extra blank space if grid is not square
    missing_cnt = len(grid_images) % grid_width
    for _ in range(missing_cnt):
        blank_im = np.zeros([grid_im_height, grid_im_width, im_depth], dtype=np.uint8)
        blank_im.fill(255)
        grid_images.append(blank_im)

    # Combine images
    rows = []
    row_cnt = len(grid_images) // grid_width
    for i in range(row_cnt):
        start, end = i * grid_width, (i + 1) * grid_width
        rows.append(cv2.hconcat(grid_images[start:end]))
    grid = cv2.vconcat(rows)

    # Save grid image
    cv2.imwrite(f"./{file_name}", grid)


def main():
    """
    Filters each image in directory then prints warnings for abnormal images
    """
    # Convert input ranges into integers
    raw_filter = vars(args).copy()
    raw_filter.pop("frames_dir")
    raw_filter.pop("value_thresh")
    raw_filter.pop("size_thresh")
    name_filter = get_filter_ranges(raw_filter)

    # Filter and read in image info
    images_info = get_images_info(args.frames_dir, name_filter, extension)

    # Check for odd images
    find_small_images(images_info, args.size_thresh)
    find_black_images(images_info, args.value_thresh)

    # Output
    print_report(images_info)
    create_warning_image_grid(images_info)


if __name__ == '__main__':
    naming_words, extension = load_naming_convention(NAMING_CONVENTION_TXT)

    parser = argparse.ArgumentParser(
        description="This tool helps identify broken frames. "
                    "The naming conventions of the frames can be set in 'naming.txt'. "
                    "This can be used to filter out which frames to analyze. "
                    "Ex: With naming convention 'scene_shot_frame.png', you may add the parameter "
                    "'--scene 001' or '--shot 1000-1005")
    parser.add_argument("frames_dir", help="Directory of frames", type=str)
    parser.add_argument("--value_thresh", help="Threshold of value for dark frames."
                                               "Default is '0.0' (completely black)",
                        type=float, default=0.01)
    parser.add_argument("--size_thresh", help="Threshold of file size in MB."
                                              "Defaults is '0.2' (0.2MB)",
                        type=float, default=.2)
    for word in naming_words:
        parser.add_argument(f"--{word}", help=f"Filter the {word} # of the frame. "
                                              f"Ex: '--{word} 001' or  '--{word} 5-10'",
                            type=str)
    args = parser.parse_args()

    main()
