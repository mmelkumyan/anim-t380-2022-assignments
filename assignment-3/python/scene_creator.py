"""Creates empty group in scene with asset name"""

import os
import argparse
import maya.standalone

maya.standalone.initialize()
import maya.cmds

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="This script creates a scene with an empty group.")
    parser.add_argument("-asset", help="The asset the scene is named after. "
                                       "If none is proved will default to argument "
                                       "variable '$asset'", type=str, default="")
    args = parser.parse_args()

    # Get asset name from env variable if no argument passed
    asset_name = args.asset if args.asset else str(os.getenv('asset'))

    # Create empty group
    maya.cmds.group(em=True, name="empty_group")

    # Save scene
    maya.cmds.file(rename=asset_name + ".ma")
    print(f"Saving to: \'{maya.cmds.file(save=True, type='mayaAscii')}\'")
