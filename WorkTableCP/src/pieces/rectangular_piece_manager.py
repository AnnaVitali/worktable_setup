import numpy as np
import sympy
from sympy import Polygon
from skimage import draw

class RectangularPiece():

    def __init__(self, up_left_vertex, down_right_vertex, heat_map, support_area):
        self.start_x, self.start_y = up_left_vertex
        self.end_x, self.end_y = down_right_vertex
        self.heat_map = heat_map
        self.width  = self.end_x - self.start_x
        self.height = self.end_y - self.start_y
        self.support_area = support_area
        self.side_support_area = round(np.sqrt(self.support_area))
        self.rectangle = self.__instantiate_rectangle()

    def __instantiate_rectangle(self):
        return Polygon((self.start_x, self.start_y), (self.end_x, self.start_y), (self.end_x, self.end_y),
                       (self.start_x, self.end_y))

    def __translate(self, values, range_min, range_max):
        min_value  = np.min(values)
        max_value = np.max(values)
        return np.array([range_min + (range_max - range_min) * (value - min_value) / (max_value - min_value)
                         for value in values]).astype(np.int64)


    def __highlight_area_small_rectangle(self, num_tiers):
        scores = np.zeros((self.height, self.width), dtype=int)
        min_x = 0
        min_y = 0
        max_x = self.width
        max_y = self.height

        for i in range(1, num_tiers + 1):
            if (min_x <= max_x and min_y <= max_y):
                scores[min_y:max_y, min_x: min_x + self.side_support_area] = i
                scores[min_y:max_y, max_x - self.side_support_area: max_x] = i
                scores[min_y: min_y + self.side_support_area, min_x:max_x] = i
                scores[max_y - self.side_support_area:max_y, min_x:max_x] = i

                min_x += self.side_support_area
                min_y += self.side_support_area
                max_x -= self.side_support_area
                max_y -= self.side_support_area
        return scores

    def __highlight_area_big_rectangle(self, num_tiers):
        offset = int(self.side_support_area / 2)
        scores = np.zeros((self.height, self.width), dtype=int)
        min_x = 0
        min_y = 0
        max_x = self.width
        max_y = self.height

        centroid_x, centroid_y = self.rectangle.centroid.coordinates
        centroid_x = round(centroid_x.evalf())
        centroid_y = round(centroid_y.evalf())

        # the side of the square should be as long as the support
        min_center_x = centroid_x - offset
        min_center_y = centroid_y - offset
        max_center_x = centroid_x + offset
        max_center_y = centroid_y + offset

        for i in range(num_tiers, 0, -1):
            if (min_center_y > min_y and min_center_x > min_x and max_center_y < max_y and max_center_x < max_x):
                scores[min_center_y: max_center_y, min_center_x: min_center_x + offset] = i
                scores[min_center_y: max_center_y, max_center_x - offset: max_center_x] = i
                scores[min_center_y: min_center_y + offset, min_center_x:max_center_x] = i
                scores[max_center_y - offset:max_center_y, min_center_x:max_center_x] = i

                scores[min_y:max_y, min_x: min_x + self.side_support_area] = i
                scores[min_y:max_y, max_x - self.side_support_area: max_x] = i
                scores[min_y: min_y + self.side_support_area, min_x:max_x] = i
                scores[max_y - self.side_support_area:max_y, min_x:max_x] = i

                min_center_x -= offset
                min_center_y -= offset
                max_center_x += offset
                max_center_y += offset

                min_x += self.side_support_area
                min_y += self.side_support_area
                max_x -= self.side_support_area
                max_y -= self.side_support_area

        return scores

    def highlight_area(self):
        centroid_x, centroid_y = self.rectangle.centroid.coordinates
        # For the vertical line inertia axis: x = center_x
        # For the horizontal line inertia axis: y = center_y
        centroid_x = round(centroid_x.evalf())
        centroid_y = round(centroid_y.evalf())

        rr, cc = draw.rectangle((self.start_y, self.start_x), end=(self.end_y, self.end_x), shape=self.heat_map.shape)
        dist_to_vertical_line = np.abs(cc - centroid_x).astype(np.int64)
        dist_to_horizontal_line = np.abs(rr - centroid_y).astype(np.int64)

        dist_to_vertical_line = self.__translate(dist_to_vertical_line, 0, 100)
        dist_to_horizontal_line = self.__translate(dist_to_horizontal_line, 0, 100)

        self.heat_map[rr, cc] += dist_to_vertical_line
        self.heat_map[rr, cc] += dist_to_horizontal_line


        # num_tiers = round((min(self.width, self.height) / 2) / self.side_support_area)
        # print(f'is small rectangle? {round(self.height / self.side_support_area) < 5}')
        # print(round(self.height / self.side_support_area))
        # if round(self.height / self.side_support_area) < 5:
        #     scores = self.__highlight_area_small_rectangle(num_tiers)
        # else:
        #     scores = self.__highlight_area_big_rectangle(num_tiers)
        # self.heat_map[self.start_y:self.end_y, self.start_x:self.end_x] = scores






