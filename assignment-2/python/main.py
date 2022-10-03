import maya.standalone

maya.standalone.initialize()

import maya.cmds


def save(filename="example.ma"):
    maya.cmds.file(rename=filename)
    print(f"Saving to: \'{maya.cmds.file(save=True, type='mayaAscii')}\'")


if __name__ == '__main__':
    print("hello world!")

    print("Creating a cube...")
    maya.cmds.polyCube()
    maya.cmds.move(9, 9, 3)

    print(maya.cmds.ls(geometry=True))

    save()
