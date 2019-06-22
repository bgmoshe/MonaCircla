# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:19:35 2019

@author: barak
"""
from numpy.random import choice


def calculate_l1_penalty(original_image, current_image):
    penalty = 0
    size = original_image.size
    for i in range(size[0]):
        for j in range(size[1]):
            source_pixel = original_image.getpixel((i, j))
            dest_pixel = current_image.getpixel((i, j))
            penalty += sum([abs(source_pixel[k] - dest_pixel[k]) for k in range(3)])
    return penalty


def sgd(starting_point, learning_rate, function, gradient_function, iterations=0, error_rate=0):
    i = iterations
    current_error_rate = function(starting_point)
    current_point = starting_point
    while i != 0 or current_error_rate > error_rate:
        current_index = choice(len(starting_point))
        current_point[current_index] = current_point[current_index] \
            - learning_rate*gradient_function(current_point)[current_index]
        if i > 0:
            i -= 1
        current_error_rate = function(current_point)
    return current_point
