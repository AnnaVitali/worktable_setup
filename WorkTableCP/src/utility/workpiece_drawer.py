import numpy as np
from utility.line_drawer import LineDrawer
from utility.rectangle_drawer import RectangleDrawer
from utility.circle_drawer import CircleDrawer
from parameter.workings import Workings

class WorkpieceDrawer():

    def __init__(self, workpiece_width, workpiece_height):
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.workpiece_processing = np.zeros((workpiece_height, workpiece_width))
        self.line_drawer = LineDrawer()
        self.rectangle_drawer = RectangleDrawer()
        self.circle_drawer = CircleDrawer()

    def draw_perimeter_piece(self):
        for i in range(self.workpiece_height):
            if i == 0 or i == self.workpiece_height - 1:
                for j in range(self.workpiece_width):
                    self.workpiece_processing[i][j] = Workings.PERIMETER_POINT.value
            else:
                self.workpiece_processing[i][0] = Workings.PERIMETER_POINT.value
                self.workpiece_processing[i][-1] = Workings.PERIMETER_POINT.value

    def draw_line(self, start_coordinates, end_coordinates):
        self.line_drawer.draw_line(start_coordinates, end_coordinates, self.workpiece_processing,
                                   Workings.PASS_THROUGH_WORKING_POINT)

    def draw_thick_line(self, start_coordinates, end_coordinates, thickness, thickness_direction):
        self.line_drawer.draw_thick_line(start_coordinates, end_coordinates, self.workpiece_processing,
                                         Workings.PASS_THROUGH_WORKING_POINT.value, thickness, thickness_direction)

    def draw_rectangle_line(self, start_coordinates, end_coordinates, thickness = 1):
        self.rectangle_drawer.draw_rectangle(start_coordinates, end_coordinates, self.workpiece_processing,
                                             Workings.PASS_THROUGH_WORKING_POINT.value, thickness)

    def draw_circle_line(self, center_coordinates, radius, thickness = 1):
        self.circle_drawer.draw_circle(center_coordinates, radius, self.workpiece_processing,
                                       Workings.PASS_THROUGH_WORKING_POINT.value, thickness)

    def get_workpiece_processing_draw(self):
        return self.workpiece_processing
