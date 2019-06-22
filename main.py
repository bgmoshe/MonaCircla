# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:15:47 2019

@author: barak
"""

from PIL import Image
from visualizer import visualize
from approximateImage import ApproximatedImage
from sys import argv as args
from visualizer import visualize as process_visualizer

DEFAULT_MAX_CIRCLES = 200


if __name__ == "__main__":
    args = args[1:]
    #TODO add parameter flags
    if len(args) < 1 or len(args) > 2:
        print("usage: main.py image [maxCircles] \n")
        exit()
    if len(args) == 1:
        max_circles = DEFAULT_MAX_CIRCLES
    else:
        max_circles = args[1]
        args[:2]
    image_path = args[0]
    image = Image.open(image_path)
    im = ApproximatedImage(image, max_circles)
    im.optimize()
    modified_filename = image_path.split(".")
    modified_filename = modified_filename[0] + "_approximated_by_%d_circles" % max_circles
    im.get_current_image().save(modified_filename + ".jpg")
    visualize(im.images_by_steps, modified_filename + ".avi")
