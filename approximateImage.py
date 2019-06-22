from optimizer import sgd, calculate_l1_penalty, local_l1_loss_function
from PIL import Image
from imageCircle import ImageCircle
from scipy.misc import toimage
import numpy as np
from random import uniform
from time import time
from imageUtils import filter_in_points_in_image, get_average_color_by_shape


class ApproximatedImage:
    def __init__(self,
                 image,
                 max_circles,
                 optimize_function=sgd):

        self.origImage = image
        self.image_size = image.size
        self.optimize_function = optimize_function
        self.max_circles = max_circles
        self.circles = [ImageCircle(int(uniform(0, 20)),
                                    int(uniform(0, 20)),
                                    int(uniform(5, 25)),
                                    int(uniform(50, 200)),
                                    int(uniform(50, 200)),
                                    int(uniform(50, 200)),
                                    1/self.max_circles) for i in range(self.max_circles)]

        self.currentImage = Image.new(mode="RGB", size=self.image_size)#
        self.currentImage = self.calculate_image()
        self.images_by_steps = [self.currentImage]
        self.current_loss = calculate_l1_penalty(self.origImage, self.currentImage)

    def init_pixels_alphas(self):
        pixels_total_alpha = np.zeros(self.origImage.size)
        for c in self.circles:
            for point in c.get_all_contained_integer_points():
                pixels_total_alpha[point] += c.get_opacity()
        self.pixels_total_alpha = pixels_total_alpha

    def calculate_image(self):
        width, height = self.image_size
        new_image_pixels = np.zeros((width, height, 3), dtype=np.uint8)
        pixels_total_alpha = np.zeros(self.image_size)
        for c in self.circles:
            for point in c.get_all_contained_integer_points():
                new_image_pixels[point] = [(new_image_pixels[point][i] * pixels_total_alpha[point] + \
                                            c.get_rgb()[i] * c.get_opacity()) / \
                                            (pixels_total_alpha[point] + c.get_opacity()) for i in range(3)]

                pixels_total_alpha[point] += c.get_opacity()

        self.pixels_total_alpha = pixels_total_alpha

        for val in zip(*np.nonzero(new_image_pixels)):
            new_image_pixels[val] = int(round(new_image_pixels[val]))
        return toimage(new_image_pixels)

    def update_image_by_circle(self, old_circle, new_circle, circle_num):
        old_circle_points = old_circle.get_all_contained_integer_points()
        new_current_circle_points = new_circle.get_all_contained_integer_points()
        points_affected = old_circle_points + new_current_circle_points
        points_affected = filter_in_points_in_image(points_affected, self.image_size)
        pixelMap = self.currentImage.load()
        for point in points_affected:
            old_pixel_opacity = self.pixels_total_alpha[point]
            if old_circle.contains_point(point[0], point[1]):
                self.pixels_total_alpha[point] -= old_circle.get_opacity()
            if new_circle.contains_point(point[0], point[1]):
                self.pixels_total_alpha[point] += new_circle.get_opacity()
            new_pixel_value = [pixelMap[point][k] * old_pixel_opacity for k in range(3)]
            if old_circle.contains_point(point[0], point[1]):
                new_pixel_value = [new_pixel_value[k] - (old_circle.get_rgb()[k] * old_circle.get_opacity()) for k in range(3)]
            if new_circle.contains_point(point[0], point[1]):
                new_pixel_value = [new_pixel_value[k] + (new_circle.get_rgb()[k] * new_circle.get_opacity()) for k in range(3)]
            #If this was the only point in the circle, then the opacity and color will be 0
            #O/w we need to normalize the pixel value.
            if self.pixels_total_alpha[point] != 0:
                new_pixel_value = [new_pixel_value[k] / self.pixels_total_alpha[point] for k in range(3)]
            new_pixel_value = [int(round(val)) for val in new_pixel_value]
            pixelMap[point] = tuple(new_pixel_value)
        self.currentImage.save("HoHo_%d.jpg" % circle_num)

    def calculate_circle_probs(self):
        probs = [0.00001] * self.max_circles
        for circle_index, c in enumerate(self.circles):
            contained_points = c.get_all_contained_integer_points()
            for point in contained_points:
                if point[0] < 0 or point[0] > 399 or point[1] < 0 or point[1] > 399:
                    continue
                source_pixel = self.origImage.getpixel(point)
                current_pixel = self.currentImage.getpixel(point)
                current_penality = sum([abs(source_pixel[l] - current_pixel[l]) for l in range(3)])
                probs[circle_index] += current_penality
        probs_sum = sum(probs)
        probs = [p/probs_sum for p in probs]
        return probs

    def mutation_score(self, current_circle_index, new_circle):
        current_circle = self.circles[current_circle_index]
        current_circle_points = current_circle.get_all_contained_integer_points()
        new_current_circle_points = new_circle.get_all_contained_integer_points()
        points_affected = current_circle_points + new_current_circle_points
        points_affected = filter_in_points_in_image(points_affected, self.image_size)
        points_affected = list(set(points_affected))
        points_affected.sort(key=lambda x: x[0])
        mutation_score = 0
        for point in points_affected:
            previous_opacity = self.pixels_total_alpha[point]
            new_opacity =  previous_opacity
            dest_pixel_value = list(self.currentImage.getpixel(point))

            if current_circle.contains_point(point[0], point[1]):

                new_opacity -= current_circle.get_opacity()
                dest_pixel_value = [dest_pixel_value[i] -
                                    (current_circle.get_rgb()[i] * current_circle.get_opacity()) for i in range(3)]

            elif new_circle.contains_point(point[0], point[1]):
                new_opacity += new_circle.get_opacity()

                dest_pixel_value = [dest_pixel_value[i] +
                                    (new_circle.get_rgb()[i] * new_circle.get_opacity()) for i in range(3)]

            if new_opacity == 0:
                dest_pixel_value = [0, 0, 0]
            else:
                dest_pixel_value = [dest_pixel_value[i]/new_opacity for i in range(3)]

            dest_pixel_value = [int(round(dest_pixel_value[i])) for i in range(3)]

            original_pixel_value = self.origImage.getpixel(point)
            previous_pixel = self.currentImage.getpixel(point)

            prev_pixel_loss = sum([abs(previous_pixel[i] - original_pixel_value[i]) for i in range(3)])
            new_pixel_loss = sum([abs(dest_pixel_value[i] - original_pixel_value[i]) for i in range(3)])

            mutation_score += new_pixel_loss - prev_pixel_loss
        return mutation_score

    #TODO: consider this soft mutation thingy
    #def soft_mutate(self, circle_num):
    #    current_circle = self.circles[circle_num]
    #    param_to_mutate = uniform(0, 1)
    #    if param_to_mutate <= 7 / 8:
    #        print("mutate coordinates")
    #        random_x_center, random_y_center = int(uniform(5, 395)), int(uniform(5, 395))
    #        random_radius = int(uniform(10, 110))
    #        new_circle = ImageCircle(x_center=random_x_center,
    #                                 y_center=random_y_center,
    #                                 radius=random_radius,
    #                                 red=current_circle.get_red(),
    #                                 green=current_circle.get_green(),
    #                                 blue=current_circle.get_blue(),
    #                                 opacity=current_circle.get_opacity())
    #        circles_not_mutated = self.circles[:circle_num] + self.circles[circle_num + 1:]
    #        if not new_circle.intersects_with_circles_list(circles_not_mutated):
    #            print("***Woho", circle_num)
    #            points_affected = new_circle.getAllContainedIntegerPoints()
    #            points_affected = list(filter_in_points_in_image(points_affected, self.image_size))
    #            avg_color = [0, 0, 0]
    #            for p in points_affected:
    #                avg_color = [avg_color[i] + self.origImage.getpixel(p)[i] for i in range(3)]
    #            avg_color = [int(round(col / len(points_affected))) for col in avg_color]
    #            new_circle.set_rgb(tuple(avg_color))
    #            new_circle.set_opacity(0.8)
#
    #    elif param_to_mutate <= 2 / 8:
    #        print("mutate radius")
    #        random_radius = int(uniform(5, 195))
    #        new_circle = ImageCircle(x_center=current_circle.x_center,
    #                                 y_center=current_circle.y_center,
    #                                 radius=random_radius,
    #                                 red=current_circle.get_red(),
    #                                 green=current_circle.get_green(),
    #                                 blue=current_circle.get_blue(),
    #                                 opacity=current_circle.get_opacity())
    #        # print("Checking radius of %s" % random_radius)
    #    elif param_to_mutate <= 3 / 8:
    #        print("Mutate color and opacity")
    #        self.sgd_color(circle_num)
    #        which_color_to_change = int(uniform(1, 4))
    #        color_value = int(uniform(0, 256))
    #        if which_color_to_change == 1:
    #            new_circle = ImageCircle(x_center=current_circle.x_center,
    #                                     y_center=current_circle.y_center,
    #                                     radius=current_circle.radius,
    #                                     red=color_value,
    #                                     green=current_circle.get_green(),
    #                                     blue=current_circle.get_blue(),
    #                                     opacity=current_circle.get_opacity())
#
    #        elif which_color_to_change == 2:
    #            new_circle = ImageCircle(x_center=current_circle.x_center,
    #                                     y_center=current_circle.y_center,
    #                                     radius=current_circle.radius,
    #                                     red=current_circle.get_red(),
    #                                     green=color_value,
    #                                     blue=current_circle.get_blue(),
    #                                     opacity=current_circle.get_opacity())
#
    #        elif which_color_to_change == 3:
    #            new_circle = ImageCircle(x_center=current_circle.x_center,
    #                                     y_center=current_circle.y_center,
    #                                     radius=current_circle.radius,
    #                                     red=current_circle.get_red(),
    #                                     green=current_circle.get_green(),
    #                                     blue=color_value,
    #                                     opacity=current_circle.get_opacity())

    def hard_mutation(self, circle_num):
        random_x_center, random_y_center = int(uniform(5, 395)), int(uniform(5, 395))
        random_radius = int(uniform(5, 150))
        new_circle = ImageCircle(x_center=random_x_center,
                                 y_center=random_y_center,
                                 radius=random_radius,
                                 red=0,
                                 green=0,
                                 blue=0,
                                 opacity=0.5)
        rgb = get_average_color_by_shape(self.origImage, new_circle)
        new_circle.set_rgb(rgb)
        circles_not_mutated = self.circles[:circle_num] + self.circles[circle_num + 1:]
        #if new_circle.intersects_with_circles_list(circles_not_mutated):
        #    new_params = self.optimize_color_and_opacity(circle_num, new_circle)
        #    new_params[0] = int(round(new_params[0]))
        #    new_params[1] = int(round(new_params[1]))
        #    new_params[2] = int(round(new_params[2]))
        #    new_circle.set_rgb(new_params[:-1])
        #    new_circle.set_opacity(*new_params[-1:])
        return new_circle

    def optimize(self, constraint="time", time_constraint=5.0, number_of_iteration=0):
        if constraint == "time":
            current_time = time()/60
            i = 0
            while (time()/60) - current_time < time_constraint:
                i += 1
                print("Iteration %d begins" % i)
                self.mutate()
        elif constraint == "iterations":
            for i in range(number_of_iteration):
                print("Iteration %d begins" % i)
                self.mutate()

    def mutate(self):
        #Possible to pick circle in a smarter way
        #circle_probs = self.calculate_circle_probs()
        #circle_num = np.random.choice(200, p=circle_probs)
        g = time()
        circle_num = int(uniform(0, 200))
        current_circle = self.circles[circle_num]
        new_circle = self.hard_mutation(circle_num)

        mutation_score = self.mutation_score(circle_num, new_circle)

        if mutation_score <= 0:
            self.current_loss += mutation_score
            self.circles[circle_num] = new_circle
            self.update_image_by_circle(current_circle, new_circle, circle_num)
            self.images_by_steps.append(self.currentImage.copy())

    def get_current_image(self):
        return self.currentImage

    def l1_loss_derivative(self, original_image, shape_num, new_shape, rgb, opacity):
        derivatives = [0, 0, 0, 0]
        points_list = filter_in_points_in_image(new_shape.get_all_contained_integer_points(), original_image.size)
        for p in points_list:
            point_total_opacity = 0
            point_total_value = [0, 0, 0]
            point_pixel_value = [0, 0, 0]
            for i, c in enumerate(self.circles):
                if i == shape_num:
                    point_total_opacity += opacity
                    point_total_value = [point_total_value[i] + rgb[i] for i in range(3)]
                    point_pixel_value = [point_pixel_value[i] + rgb[i] * opacity for i in range(3)]

                elif c.contains_point(*p):
                    point_total_opacity += c.get_opacity()
                    point_total_value = [point_total_value[i] + c.get_rgb()[i] for i in range(3)]
                    point_pixel_value = [point_pixel_value[i] + c.get_rgb()[i]*c.get_opacity() for i in range(3)]

            pixel_value = original_image.getpixel(p)
            sign = [pixel_value[i] - (point_pixel_value[i]/point_total_opacity) for i in range(3)]
            for i in range(3):
                if sign[i] > 0:
                    sign[i] = 1
                elif sign[i] < 0:
                    sign[i] = -1
            point_rgb_derivative = [-1 * sign[i] * opacity/point_total_opacity for i in range(3)]
            point_opacity_derivative = [-1 * sign[i] *
                                        (rgb[i] * point_total_opacity - point_pixel_value[i]) /
                                        (point_total_opacity ** 2) for i in range(3)]
            point_opacity_derivative = sum(point_opacity_derivative)
            derivatives[0] += point_rgb_derivative[0]
            derivatives[1] += point_rgb_derivative[1]
            derivatives[2] += point_rgb_derivative[2]
            derivatives[3] += point_opacity_derivative
        return derivatives


    def optimize_color_and_opacity(self, current_shape_num, new_shape):
        loss_function = lambda r, g, b, opacity: local_l1_loss_function(
                                                    original_image=self.origImage,
                                                    current_shape_num=current_shape_num,
                                                    list_of_shapes=self.circles,
                                                    new_shape=new_shape,
                                                    rgb=(r, g, b),
                                                    opacity=opacity)
        loss_function_derivative = lambda r, g, b, opacity: self.l1_loss_derivative(self.origImage,
                                                                                    shape_num=current_shape_num,
                                                                                    new_shape=new_shape,
                                                                                    rgb=(r, g, b),
                                                                                    opacity=opacity)
        print("Starting sgd")
        new_params = self.optimize_function(starting_point=[new_shape.get_red(), new_shape.get_green(), new_shape.get_blue(), new_shape.get_opacity()],
                                            learning_rate=0.001,
                                            function=loss_function,
                                            gradient_function=loss_function_derivative,
                                            iterations=5)
        return new_params

    def get_all_iterations_results(self):
        return self.images_by_steps
