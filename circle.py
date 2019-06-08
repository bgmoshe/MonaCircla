# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:02:00 2019

@author: barak
"""


class Circle:
    
    def __init__(self, x_center, y_center, radius):
        self.radius = radius
        self.x_center = x_center
        self.y_center = y_center
        self.points = list()

    def getAllContainedIntegerPoints(self, save_points):
        points = list()

        #To reduce number of calculations
        if len(self.points) != 0:
            return self.points

        for offset in range(-1*self.radius, self.radius+1):
            squared_y_delta = self.radius**2 - (self.x_center + offset)**2
            current_x = self.x_center + offset
            new_points = [(current_x, y)
                          for y in range(self.y_center-self.radius, self.y_center+self.radius)
                          if (y-self.y_center)**2 <= squared_y_delta]
            points = points + new_points

        if save_points:
            self.points = points

        return points
