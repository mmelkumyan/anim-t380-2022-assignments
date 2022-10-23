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
