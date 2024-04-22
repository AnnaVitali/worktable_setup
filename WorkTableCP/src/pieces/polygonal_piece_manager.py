import numpy as np
import sympy
from sympy import Polygon
from skimage import draw

INCREMENT_VALUE = 2
AREA_VALUE = 1
CENTROID_VALUE = 4
PASS_THROUGH_WORKING = -1


class PolygonalPiece():

    def __init__(self, points, sides, workpiece_processing, support_area):
        self.points = points
        self.sides = sides
        self.support_area = support_area
        self.heat_map = workpiece_processing
        self.polygon_heat_map = np.zeros_like(self.heat_map)
        self.polygon = self.__instantiate_polygon()

    def __instantiate_polygon(self):
        return Polygon(*self.points)

    def __compute_mid_points(self):
        mid_points = []
        for index, side in enumerate(self.sides):
            start, end = side
            start_x, start_y = start
            end_x, end_y = end
            mid_x = round((end_x + start_x) / 2)
            mid_y = round((end_y + start_y) / 2)
            mid_points.append((mid_x, mid_y))
        return mid_points

    def __compute_inertia_axis(self):
        jx, jy, jxy = self.polygon.second_moment_of_area()
        centroid_x, centroid_y = self.polygon.centroid.coordinates
        alpha_x = sympy.atan2(2 * jxy, jx - jy) / 2
        m_x = sympy.tan(alpha_x)
        m_y = - 1 / m_x
        q_x = centroid_y - m_x * centroid_x
        q_y = -m_y * centroid_x + centroid_y
        return float(m_x.evalf()), float(m_y.evalf()), float(q_x.evalf()), float(q_y.evalf())

    def __draw_simple_line(self, start_coordinates, end_coordinates):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        sx = -1 if start_x > end_x else 1
        sy = -1 if start_y > end_y else 1

        x, y = start_x, start_y
        self.heat_map[y][x] += INCREMENT_VALUE

        if dx > dy:
            err = dx / 2.0
            while x != end_x:
                self.heat_map[y][x] += INCREMENT_VALUE
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != end_y:
                self.heat_map[y][x] += INCREMENT_VALUE
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

    def __compute_distance_between_point_and_line(self, point, m, q):
        return int(abs(m * point[0] - point[1] + q) / np.sqrt(m ** 2 + 1))
    def highlight_area(self):
        mx, my, qx, qy = self.__compute_inertia_axis()

        x_cords = []
        y_cords = []
        for idx, point in enumerate(self.points):
            x, y = point.coordinates
            x_cords.append(x)
            y_cords.append(y)

        rr, cc = draw.polygon(y_cords, x_cords, self.heat_map.shape)
        score = [self.__compute_distance_between_point_and_line((x, y), mx, qx) +
                 self.__compute_distance_between_point_and_line((x, y), my, qy) for x, y in zip(cc, rr)]

        self.heat_map[rr, cc] += score

        # rr, cc = draw.polygon(y_cords, x_cords, self.heat_map.shape)
        #
        #
        # self.heat_map[centroid_y, centroid_x] += CENTROID_VALUE
        # mid_points = self.__compute_mid_points()
        #
        # x_cords = []
        # y_cords = []
        #
        # for idx, point in enumerate(self.points):
        #     x, y = point.coordinates
        #     x_cords.append(x)
        #     y_cords.append(y)
        #
        # rr, cc = draw.polygon(y_cords, x_cords, self.heat_map.shape)
        # self.heat_map[rr, cc] += AREA_VALUE
        #
        #
        # for idx, point in enumerate(mid_points):
        #     self.__draw_simple_line(point, (centroid_x, centroid_y))
        # print(f'{centroid_x},  {centroid_y}')
