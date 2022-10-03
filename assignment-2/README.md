# Assignment 2

## Description

- This script creates a parametric sphere out of default cubes.
- ![Parametric sphere](https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.songho.ca%2Fopengl%2Ffiles%2Fgl_sphere01.png&f=1&nofb=1&ipt=9cbb49b70493462ee88c03662117bd09799c84ccdae76ded3fe82271a91ec09d&ipo=images)

## Arguments

- radius: Radius of the generated sphere.
- step_size: Size of each step around sphere in degrees. A higher value yields a lower
  resolution.,

## Example

- `mayapy .\parametric_sphere_generator.py`: Uses default values `radius=5`
  and `step_size=24`.
- `mayapy .\parametric_sphere_generator.py -radius 50 -step_size 30`