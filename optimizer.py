# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 21:19:35 2019

@author: barak
"""
from numpy.random import choice

def sgd(starting_point, learning_rate, function, gradient_function, T=0, error_rate=0):
    i = T
    current_error_rate = function(starting_point)
    current_point = starting_point
    while(i!=0 or current_error_rate > error_rate):
        current_index = choice(len(starting_point))
        current_point[current_index] = current_point[current_index] \
            - learning_rate*gradient_function(current_point)[current_index]
        if(i>0):
            i -= 1
        current_error_rate = function(current_point)
    return current_point
