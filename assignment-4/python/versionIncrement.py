import maya.cmds


def incrementAndSave():
    delimiter = "."

    # Get file name and split
    file_name = maya.cmds.file(sceneName=True, shortName=True, query=True)
    asset, task, artist, version, ext = file_name.split(delimiter)

    # Increment version number
    version_num = int(version)
    version_num += 1
    version = str(version_num)

    # Save with updated file name
    updated_file_name = delimiter.join([asset, task, artist, version, ext])
    maya.cmds.file(rename=updated_file_name)
    print(f"Saving to: \'{maya.cmds.file(save=True, type='mayaAscii')}\'")


incrementAndSave()
