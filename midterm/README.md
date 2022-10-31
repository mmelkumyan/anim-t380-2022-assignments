# ANIM T380 - Midterm

## Broken Frame Analyzer

### Description

- This script analyzes a directory for broken frames. It checks for the following
  qualities:
    - Dark/ black frames
    - Frames with small files sizes

### Arguments

Positional arguments:

- `frames_dir` - Path to directory of frames

Optional arguments:

- `value_thresh` - Threshold of value for dark frames
    - Ex. `--value_thresh 0.0` gives warnings for completely black frames.
    - Ex. `--value_thresh 0.01` gives warnings for frames with an average value of 1%.
- `size_thresh` - Threshold of file size in MB. Ex.
    - Ex. `--size_thresh 20` gives warnings for frames below 20MB.
- Filter frame name depending on naming convention set in `naming.txt`. Can filter a
  single value or a range.
    - Ex. If `naming.txt` is set as `scene_shot_frame.png` then the optional parameters
      are:
        - `--scene #-#`
        - `--shot #-#`
        - `--frame #-#`
        - Where `#-#` is a range such as `001-005` or a single value such as `001`

### Example

- Naming conventions in `naming.txt` is set as `scene_shot_frame.png`.
    - This gives optional filtering arguments `--scene`, `--shot`, and `--frame`
    - Ex 1.) Run command `test_frames --scene 001 --shot 005`
        - Analyzes scene 1 shot 5 only
    - Ex 1.) Run command `test_frames --frames 1000-1100`
        - Analyzes frames 1000-1100 only
    - Possible output:

  ```
  001_005_1003.png
       Small image - Image size is 0.086721 megabytes
  001_005_1004.png
       Small image - Image size is 0.062908 megabytes
  001_005_1005.png
       Small image - Image size is 0.005023 megabytes
       Dark image - Average value of 0.44%
  ```