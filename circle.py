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

    def get_all_contained_integer_points(self, save_points="auto"):
        points = list()

        #To reduce number of calculations
        if len(self.points) != 0:
            return self.points

        for offset in range(-1*self.radius, self.radius+1):
            current_x = self.x_center + offset
            new_points = [(current_x, y)
                          for y in range(self.y_center-self.radius, self.y_center+self.radius+1)
                          if self.contains_point(current_x, y)]
            points = points + new_points

        if save_points.lower() == "true":
            self.points = points
        elif save_points.lower() == "auto" and len(points) > 1000:
            self.points = points
        return points

    def get_center(self):
        return self.x_center, self.y_center

    def get_radius(self):
        return self.radius

    def contains_point(self, x, y):
        distance = (self.x_center-x) ** 2 + (self.y_center-y) ** 2
        return distance <= self.radius ** 2

    def intersect_with_circle(self, circle):
        self_x, self_y = self.get_center()
        self_radius = self.get_radius()
        circle_x, circle_y = circle.get_center()
        circle_radius = circle.get_radius()
        centers_distance = (self_x - circle_x) ** 2 + (self_y - circle_y) ** 2
        return centers_distance <= (self_radius+circle_radius) ** 2

    def intersects_with_circles_list(self, list_of_circles):
        for circle in list_of_circles:
            if self.intersect_with_circle(circle):
                return True
        return False
