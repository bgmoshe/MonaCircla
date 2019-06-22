# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 15:02:00 2019

@author: barak
"""

from circle import Circle


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

    def set_rgb(self, rgb):
        self.rgb['red'] = rgb[0]
        self.rgb['green'] = rgb[1]
        self.rgb['blue'] = rgb[2]

    def set_opacity(self, opacity):
        self.opacity = opacity

    def __str__(self):
        return "Center = (%d, %d), Radius = %f, RGB = (%d, %d, %d), opacity=%f" % \
               (self.x_center, self.y_center,
                self.radius,
                self.get_red(), self.get_green(), self.get_blue(),
                self.get_opacity())