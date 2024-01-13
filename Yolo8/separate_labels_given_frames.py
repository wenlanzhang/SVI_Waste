"""
Script to get the text label files given the image names.
"""

import os
import shutil

IMG_PATH = os.path.join('only_rainy_frames', 'images')
TXT_PATH = os.path.join('valid', 'labels')

image_paths = os.listdir(IMG_PATH)
label_paths = os.listdir(TXT_PATH)

match_counter = 0
for i, img_name in enumerate(image_paths):
    file_name = '.'.join(img_name.split('.')[:-1])
    for j, label_name in enumerate(label_paths):
        if file_name == '.'.join(label_name.split('.')[:-1]):
            match_counter += 1
            shutil.move(
                os.path.join(TXT_PATH, label_name),
                os.path.join('only_rainy_frames', 'labels', label_name)
            )