from PIL import Image


def get_average_color_in_box(image, width, height):
    rgb = [0] * 3
    for i in range(width):
        for j in range(height):
            pixel_value = image.getpixel((i,j))
            rgb = [rgb[i] + pixel_value[i] for i in range(3)]
    rgb = [rgb[i]/(width*height) for i in range(3)]
    return rgb


def get_average_color_by_shape(image, shape):
    rgb = [0] * 3
    points = shape.get_all_contained_integer_points()
    points = filter_in_points_in_image(points, image.size)
    for p in points:
        pixel_value = image.getpixel(p)
        rgb = [rgb[i] + pixel_value[i] for i in range(3)]
    rgb = [int(round(rgb[i]/len(points))) for i in range(3)]
    return tuple(rgb)


def image_crop(image, rows_to_crop, col_to_crop):
    width, height = image.size
    width_of_cropped = width/col_to_crop
    height_of_cropped = height/rows_to_crop
    images = list()
    for i in range(rows_to_crop):
        for j in range(col_to_crop):
            left = j * width_of_cropped
            right = left + width_of_cropped
            top = i * height_of_cropped
            bottom = top + height_of_cropped
            images.append(image.crop((left, top, right, bottom)))
    return images


def image_unify(images_list, number_of_lines, number_of_cols):
    crop_width, crop_height = images_list[0].size
    result_width = crop_width * number_of_cols
    result_height = crop_height * number_of_lines
    result = Image.new('RGB', (result_width, result_height))
    curr_height, curr_image_index = 0, 0
    for i in range(number_of_lines):
        curr_width = 0
        for j in range(number_of_cols):
            result.paste(images_list[curr_image_index], (curr_width, curr_height))
            curr_image_index += 1
            curr_width += crop_width
        curr_height += crop_height
    return result


def filter_in_points_in_image(list_of_points, size):
    width, height = size
    check_if_points_contained = lambda point: (0 <= point[0] < width) and\
                                              (0 <= point[1] < height)
    new_list = filter(check_if_points_contained, list_of_points)
    return list(new_list)
