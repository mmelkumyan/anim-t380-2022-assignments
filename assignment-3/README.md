# Assignment 3

## Asset Directory Creator

### Description

- This script creates a directory `assets/$asset/maya/scenes`, where `$asset` is an
  environment variable.

### Arguments

- None

### Example

- `$ source etc/.aliases`: Loads alias `setasset`
- `$ setasset`: Sets the environment variable `$asset` to `my_asset`.
- `$ python asset_dir_creator.py`: Creates directory `assets/my_asset/maya/scenes`

## Scene Creator

### Description

- Creates an empty group in a maya scene names after the given asset. Can take the asset
  name as an argument or use an environment variable

### Arguments

- `-asset`: The asset the scene is named after. If none, uses environment
  variable `$asset`.

### Example

- `mayapy scene_creator.py`: Creates `my_asset.ma` at default location with an empty
  group.
- `mayapy scene_creator.py -asset trex`: Creates `trex.ma` at default location with an
  empty group.