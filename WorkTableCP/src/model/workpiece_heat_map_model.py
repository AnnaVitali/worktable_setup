import numpy as np
from pieces.polygonal_piece_manager import PolygonalPiece
from pieces.rectangular_piece_manager import RectangularPiece
from pieces.circle_piece_manager import CirclePiece
from parameter.workings import Workings

INCREMENT_IMPORTANCE = 1
MAXIMUM_IMPORTANCE = 2
class WorkpieceHeatMapModel():

    def __init__(self, workpiece_processing, workpiece_width, workpiece_height, support_area):
        self.workpiece_processing = workpiece_processing
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.support_area = support_area
        self.heat_map = np.zeros((workpiece_height, workpiece_width), dtype=int)

    def __highlight_perimeter(self):
        for i in range(self.workpiece_height):
            for j in range(self.workpiece_width):
                if self.workpiece_processing[i, j] == Workings.PERIMETER_POINT.value:
                    self.heat_map[i, j] += INCREMENT_IMPORTANCE

    def __highlight_pass_through_workings(self):
        self.heat_map = np.where(self.workpiece_processing == -1, self.workpiece_processing, self.heat_map)
        point_checked = []
        for i in range(self.workpiece_height):
            for j in range(self.workpiece_width):
                if self.workpiece_processing[i, j] == Workings.PASS_THROUGH_WORKING_POINT.value:
                    for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if ((0 <= i + r < self.workpiece_height) and (0 <= j + c < self.workpiece_width)
                                and not point_checked.__contains__((i + r, j + c))
                                and self.workpiece_processing[i + r, j + c] != Workings.PASS_THROUGH_WORKING_POINT.value
                                and self.workpiece_processing[i + r, j + c] <= MAXIMUM_IMPORTANCE):
                            self.heat_map[i + r, j + c] = min(
                                self.heat_map[i + r, j + c] + INCREMENT_IMPORTANCE, MAXIMUM_IMPORTANCE)
                            point_checked.append((i + r, j + c))

    def __compute_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    def report_polygonal_piece(self, points, sides):
        polygonal_peace = PolygonalPiece(points, sides, self.heat_map, self.support_area)
        polygonal_peace.highlight_area()

    def report_rectangle_piece(self, start_coordinates, end_coordinates):
        rectangular_peace = RectangularPiece(start_coordinates, end_coordinates, self.heat_map,
                                             self.support_area)
        rectangular_peace.highlight_area()

    def report_round_peace(self, center_coordinates, radius):
        circle_peace = CirclePiece(center_coordinates, radius, self.heat_map, self.support_area)
        circle_peace.highlight_area()

    def compute_heat_map(self):
        self.__highlight_perimeter()
        self.__highlight_pass_through_workings()
        return self.heat_map
