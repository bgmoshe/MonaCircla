# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:02:00 2019

@author: barak
"""

from circle import Circle

class ImageCircle(Circle):

    def __init__(self, x_center, y_center, radius, red, green, blue, opacity):
        self.rgb = {'red':red, 'green': green, 'blue': blue}
        self.opacity = opacity

    def get_red(self):
        return self.rgb['red']

    def get_blue(self):
        return self.rgb['blue']

    def get_green(self):
        return self.rgb['green']

    def get_opacity(self):
        return self.opacity
