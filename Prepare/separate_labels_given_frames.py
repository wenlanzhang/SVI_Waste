"""
Script to get the text label files given the image names.
"""

import os
import shutil

IMG_PATH = os.path.join('/Users/wenlanzhang/Downloads/PhD_UCL/Data/GoogleStreetView', 'Train')
TXT_PATH = os.path.join('/Users/wenlanzhang/Downloads/PhD_UCL/Data/GoogleStreetView', 'Train')

if __name__ == '__main__':

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
                    os.path.join('/Users/wenlanzhang/Downloads', 'Waste4Yolo', label_name)
                )

