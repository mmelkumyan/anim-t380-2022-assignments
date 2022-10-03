"""A command line script to generate parametric spheres in maya"""

import argparse
import math

import maya.standalone

maya.standalone.initialize()
import maya.cmds


def save(filename="example"):
    """
    Saves scene to a maya file.

    :param filename: Name of the file to save. Extension ".ma" is added automatically.
    """
    maya.cmds.file(rename=filename + ".ma")
    print(f"Saving to: \'{maya.cmds.file(save=True, type='mayaAscii')}\'")


def create_parametric_sphere(radius, step_size):
    """
    Generates a parametric sphere out of default cubes. Centered at the origin.
    Parametric sphere equation: https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.songho.ca%2Fopengl%2Ffiles%2Fgl_sphere01.png&f=1&nofb=1&ipt=9cbb49b70493462ee88c03662117bd09799c84ccdae76ded3fe82271a91ec09d&ipo=images

    :param radius: Radius of the generated sphere.
    :param step_size: Size of each step around sphere. A higher value yields a lower
        resolution. In degrees.
    """
    print("Creating a parametric sphere...")

    # Loop through positions on a sphere
    # Phi is latitude, theta is longitude
    for phi in range(-90, 91, step_size):
        for theta in range(0, 360, step_size):
            # Convert phi and theta to radians
            t, p = math.radians(theta), math.radians(phi)

            # Calculate position
            pos = radius * math.cos(p) * math.cos(t), \
                  radius * math.sin(p), \
                  radius * math.cos(p) * math.sin(t)

            # Generate and move cube
            maya.cmds.polyCube()
            maya.cmds.move(*pos)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="This script creates a parametric sphere out of default cubes.")
    parser.add_argument("-radius", help="Radius of the sphere.", type=float, default=5)
    parser.add_argument("-step_size",
                        help="Size of each step around sphere. "
                             "A higher value yields a lower resolution.",
                        type=int, default=24)
    args = parser.parse_args()

    create_parametric_sphere(args.radius, args.step_size)

    print(maya.cmds.ls(geometry=True))
    print("Done!")

    save()
