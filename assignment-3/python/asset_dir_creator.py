"""Creates directory 'assets/$asset/maya/scenes'"""
import os

asset_name = os.getenv('asset')

scene_path = os.path.join("assets", asset_name, "maya", "scenes")
print(f"Creating directory: '{scene_path}'")
os.makedirs(scene_path)
