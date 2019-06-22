# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:19:35 2019

@author: barak
"""
from numpy.random import choice
from imageUtils import filter_in_points_in_image


def calculate_l1_penalty(original_image, current_image):
    penalty = 0
    size = original_image.size
    for i in range(size[0]):
        for j in range(size[1]):
            source_pixel = original_image.getpixel((i, j))
            dest_pixel = current_image.getpixel((i, j))
            penalty += sum([abs(source_pixel[k] - dest_pixel[k]) for k in range(3)])
    return penalty


def local_l1_loss_function(original_image, list_of_shapes, current_shape_num, new_shape, rgb, opacity):
    points_in_shape = filter_in_points_in_image(new_shape.get_all_contained_integer_points(),
                                                original_image.size)
    loss = 0
    for p in points_in_shape:
        orig_pixel = original_image.getpixel(p)
        current_pixel_value = [0, 0, 0]
        total_opacity = 0
        for i, s in enumerate(list_of_shapes):
            if i == current_shape_num:
                current_pixel_value = [current_pixel_value[i] + rgb[i] * opacity for i in range(3)]
                total_opacity += opacity

            if s.contains_point(*p):
                current_pixel_value = [current_pixel_value[i] +
                                       (s.get_rgb()[i] * s.get_opacity()) for i in range(3)]
                total_opacity += opacity

        if total_opacity != 0:
            current_pixel_value = [val/total_opacity for val in current_pixel_value]
        else:
            current_pixel_value = [0, 0, 0]

        loss += sum([abs(orig_pixel[i] - current_pixel_value[i]) for i in range(3)])
    return loss


def sgd(starting_point, learning_rate, function, gradient_function, iterations=0, error_rate=0):
    i = iterations
   # current_error_rate = function(*starting_point)
    current_point = starting_point
    while i != 0:#or current_error_rate > error_rate:
        if i > 0:
            print("Begin sgd iteration i=%d" % (iterations - i +1))
            i -= 1
        current_index = choice(len(starting_point))
        current_point[current_index] = current_point[current_index] \
            - learning_rate*(gradient_function(*current_point)[current_index])

    #    current_error_rate = function(*current_point)
    return current_point
