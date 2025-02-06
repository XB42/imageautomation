#!/usr/bin/env python3
import os

def recreate_folders():
    source_folder = 'images'
    dest_folder = 'recreated_images'
    image_paths = []

    # Check if the source folder exists
    if not os.path.isdir(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return image_paths

    # Walk through the source folder and recreate the directory structure
    for root, dirs, files in os.walk(source_folder):
        rel_path = os.path.relpath(root, source_folder)
        new_dir = os.path.join(dest_folder, rel_path)
        os.makedirs(new_dir, exist_ok=True)


