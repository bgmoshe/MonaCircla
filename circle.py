# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:02:00 2019

@author: barak
"""

from random import uniform

class Circle:
    
    def __init__(self, x_center, y_center, radius):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center
        self.points = list()

    def getAllContainedIntegerPoints(self, save_points=False):
        points = list()

        #To reduce number of calculations
        if len(self.points) != 0:
            return self.points

        for offset in range(-1*self.radius, self.radius+1):
            current_x = self.x_center + offset
            new_points = [(current_x, y)
                          for y in range(self.y_center-self.radius, self.y_center+self.radius+1)
                          if self.check_if_contains_point(current_x, y)]
            points = points + new_points

        if save_points:
            self.points = points

        return points

    def check_if_contains_point(self, x, y):
        distance = (self.x_center-x) ** 2 + (self.y_center-y) ** 2
        return distance <= self.radius ** 2


def generate_random_circle(width, height, max_radius):
    x = uniform(0, width - 0.1)
    y = uniform(0, height - 0.1)
    r = uniform(1, max_radius+1)
    circle = Circle(x_center=int(x), y_center=int(y), radius=int(r))
    return circle
