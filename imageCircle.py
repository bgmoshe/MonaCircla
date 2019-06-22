# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:02:00 2019

@author: barak
"""

from circle import Circle, generate_random_circle
from random import  uniform

class ImageCircle(Circle):

    def __init__(self, x_center, y_center, radius, red, green, blue, opacity):
        super().__init__(x_center, y_center, radius)
        self.rgb = {'red': red, 'green': green, 'blue': blue}
        self.opacity = opacity

    def get_red(self):
        return self.rgb['red']

    def get_blue(self):
        return self.rgb['blue']

    def get_green(self):
        return self.rgb['green']

    def get_opacity(self):
        return self.opacity

    def get_rgb(self):
        return self.rgb['red'], self.rgb['green'], self.rgb['blue']

    def __str__(self):
        return "Center = (%d, %d), Radius = %f, RGB = (%d, %d, %d), opacity=%f" % \
               (self.x_center, self.y_center,
                self.radius,
                self.get_red(), self.get_green(), self.get_blue(),
                self.get_opacity())

def generate_random_image_circle(width, height, max_radius):
    c = generate_random_circle(width=width, height=height, max_radius=max_radius)
    x, y, r = c.x_center, c.y_center, c.radius
    opacity = uniform(0, 1)
    red = uniform(0, 256 - 0.1)
    green = uniform(0, 256 - 0.1)
    blue = uniform(0, 256 - 0.1)
    image_circle = ImageCircle(x_center=x, y_center=y, radius=r, red=red, green=green, blue=blue, opacity=opacity)
    return image_circle
