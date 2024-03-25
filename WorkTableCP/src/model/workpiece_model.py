import numpy as np
from skimage import draw

PASS_THROUGH_WORKING_POINT = -1
PERIMETER_POINT = 1
INCREMENT_IMPORTANCE = 1
MAXIMUM_IMPORTANCE = 2

class WorkpieceModel():

    def __init__(self, workpiece_processing, workpiece_width, workpiece_height):
        self.workpiece_processing = workpiece_processing
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.heat_map_model = np.zeros((workpiece_height,  workpiece_width), dtype=int)

    def __highlight_perimeter(self):
        for i in range(self.workpiece_height):
            for j in range(self.workpiece_width):
                if self.workpiece_processing[i, j] == PERIMETER_POINT:
                    self.heat_map_model[i, j] += INCREMENT_IMPORTANCE

    def __highlight_pass_through_workings(self):
        self.heat_map_model = np.where(self.workpiece_processing == -1, self.workpiece_processing,   self.heat_map_model)
        for i in range(self.workpiece_height):
            for j in range(self.workpiece_width):
                if self.workpiece_processing[i, j] == PASS_THROUGH_WORKING_POINT:
                    for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if (0 <= i + r < self.workpiece_height) and (0 <= j + c < self.workpiece_width):
                            if (self.workpiece_processing[i + r, j + c] != PASS_THROUGH_WORKING_POINT
                                    and self.workpiece_processing[i + r, j + c] <= MAXIMUM_IMPORTANCE):
                                self.heat_map_model[i + r, j + c] += INCREMENT_IMPORTANCE

    def report_polygonal_piece(self, start_vertex_coordinates, end_vertex_coordinates):
        rr, cc = draw.polygon(end_vertex_coordinates, start_vertex_coordinates, shape=self.heat_map_model.shape)
        self.heat_map_model[rr, cc] = np.where(self.workpiece_processing[rr, cc] != PASS_THROUGH_WORKING_POINT,
                                            self.heat_map_model[rr, cc] + INCREMENT_IMPORTANCE,
                                            self.heat_map_model[rr, cc])

    def report_rectangle_piece(self, start_coordinates, end_coordinates):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates

        for i in range(start_y, end_y):
            for j in range(start_x, end_x):
                self.heat_map_model[i, j] = np.where(self.workpiece_processing[i, j] != PASS_THROUGH_WORKING_POINT
                                                     and self.workpiece_processing[i, j] <= MAXIMUM_IMPORTANCE,
                                            self.heat_map_model[i, j] + INCREMENT_IMPORTANCE,
                                            self.heat_map_model[i, j])

    def report_round_peace(self, center_coordinates, radius):
        center_x, center_y = center_coordinates

        for i in range(len(self.heat_map_model[0])):
            for j in range(len(self.heat_map_model[1])):
                if (i - center_y) ** 2 + (j - center_x) ** 2 <= radius ** 2:
                    self.heat_map_model[i, j] = np.where(self.workpiece_processing[i, j] != PASS_THROUGH_WORKING_POINT
                                                         and self.workpiece_processing[i, j] <= MAXIMUM_IMPORTANCE,
                                            self.heat_map_model[i, j] + INCREMENT_IMPORTANCE,
                                            self.heat_map_model[i, j])

    def compute_heat_map(self):
        self.__highlight_perimeter()
        self.__highlight_pass_through_workings()
        return self.heat_map_model


