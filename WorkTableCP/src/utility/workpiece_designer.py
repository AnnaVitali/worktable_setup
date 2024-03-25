import numpy as np
from skimage import draw

PASS_THROUGH_WORKING_POINT = -1
PERIMETER_POINT = 1

class WorkpieceDesigner():

    def __init__(self, workpiece_width, workpiece_height):
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.workpiece_processing = np.zeros((workpiece_height, workpiece_width))

    def draw_perimeter_piece(self):
        for i in range(self.workpiece_height):
            if i == 0 or i == self.workpiece_height - 1:
                for j in range(self.workpiece_width):
                    self.workpiece_processing[i][j] = PERIMETER_POINT
            else:
                self.workpiece_processing[i][0] = PERIMETER_POINT
                self.workpiece_processing[i][-1] = PERIMETER_POINT

    def draw_simple_line(self, start_coordinates, end_coordinates):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        sx = -1 if start_x > end_x else 1
        sy = -1 if start_y > end_y else 1

        x, y = start_x, start_y
        self.workpiece_processing[y][x] = PASS_THROUGH_WORKING_POINT

        if dx > dy:
            err = dx / 2.0
            while x != end_x:
                self.workpiece_processing[y][x] = PASS_THROUGH_WORKING_POINT
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != end_y:
                self.workpiece_processing[y][x] = PASS_THROUGH_WORKING_POINT
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

    def draw_thick_line(self, start_coordinates, end_coordinates, thickness, thickness_direction):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates

        match thickness_direction:
                case "down":
                    for i in range(thickness):
                        y1 = max(start_y - i, 0)
                        y2 = max(end_y - i, 0)
                        self.draw_simple_line((start_x, y1), (end_x, y2))

                case "up":
                    for i in range(thickness):
                        y1 = min(start_y + i, self.workpiece_height - 1)
                        y2 = min(end_y + i, self.workpiece_height - 1)
                        self.draw_simple_line((start_x, y1), (end_x, y2))
                case "left":
                    for i in range(thickness):
                        x1 = max(start_x - i, 0)
                        x2 = max(end_x - i, 0)
                        self.draw_simple_line((x1, start_y), (x2, end_y))
                case "right":
                    for i in range(thickness):
                        x1 = min(start_x + i, self.workpiece_width - 1)
                        x2 = min(end_x + i, self.workpiece_width - 1)
                        self.draw_simple_line((x1, start_y), (x2, end_y))


    def draw_rectangle_line(self, start_coordinates, end_coordinates, thickness = 1):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates

        for i in range(thickness):
            # horizontal sides
            for x in range(start_x, end_x):
                self.workpiece_processing[start_y + i, x] = PASS_THROUGH_WORKING_POINT  # Assuming white color for drawing
                self.workpiece_processing[end_y - i, x] = PASS_THROUGH_WORKING_POINT  # Assuming white color for drawing

            # vertical sides
            for y in range(start_y, end_y):
                self.workpiece_processing[y, start_x + i] = PASS_THROUGH_WORKING_POINT  # Assuming white color for drawing
                self.workpiece_processing[y, end_x - i] = PASS_THROUGH_WORKING_POINT

    def draw_circle_line(self, center_coordinates, radius, thickness = 1):
            for r in range(self.workpiece_processing.shape[0]):
                for c in range(self.workpiece_processing.shape[1]):
                    distance = np.sqrt((r - center_coordinates[0]) ** 2 + (c - center_coordinates[1]) ** 2)
                    if radius <= distance <= radius + thickness:
                        self.workpiece_processing[r, c] = PASS_THROUGH_WORKING_POINT

    def get_workpiece_processing_draw(self):
        return self.workpiece_processing
