import numpy as np
import math

from src.parameter.machine import Machine


class SuctionCup:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.padding = 5
        self.rotation_angle = 0
        self.up_corner_sx = (0, 0)
        self.down_corner_sx = (0, height)
        self.up_corner_dx = (width, 0)
        self.down_corner_dx = (width, height)
        self.matrix_representation, self.matrix_representation_with_support = self.__compute_matrix_representation()
        self.center_of_rotation_x, self.center_of_rotation_y = self.__compute_center_of_rotation()

    def __rotate_point(self, x, y, angle):
        angle_in_radians = math.radians(angle)
        x_new = (x - self.center_of_rotation_x) * math.cos(angle_in_radians) - (y - self.center_of_rotation_y) * math.sin(angle_in_radians) + self.center_of_rotation_x
        y_new = (x - self.center_of_rotation_x) * math.sin(angle_in_radians) + (y - self.center_of_rotation_y) * math.cos(angle_in_radians) + self.center_of_rotation_y
        return x_new, y_new

    def __rotate_corners(self, angle):
        self.up_corner_sx = self.__rotate_point(*self.up_corner_sx, angle)
        self.down_corner_sx = self.__rotate_point(*self.down_corner_sx, angle)
        self.up_corner_dx = self.__rotate_point(*self.up_corner_dx, angle)
        self.down_corner_dx = self.__rotate_point(*self.down_corner_dx, angle)

    def __compute_matrix_representation(self):
        suction_cup_representation = np.full((self.height, self.width), 2, dtype=int)
        support_size = Machine.SUCTION_CUPS_SUPPORT_DIMENSION.value

        required_width = max(support_size, self.width) + 2 * self.padding
        required_height = max(support_size, self.height) + 2 * self.padding
        matrix = np.zeros((required_height, required_width), dtype=int)

        support_start_row = (required_height - support_size) // 2
        support_start_col = (required_width - support_size) // 2
        matrix[support_start_row:support_start_row + support_size, support_start_col:support_start_col + support_size] = 1

        suction_cup_start_row = support_start_row
        suction_cup_start_col = (required_width - self.width) // 2
        matrix[suction_cup_start_row:suction_cup_start_row + self.height, suction_cup_start_col:suction_cup_start_col + self.width] = suction_cup_representation

        return suction_cup_representation, matrix

    def __compute_center_of_rotation(self):
        return self.matrix_representation_with_support.shape[0] // 2, self.matrix_representation_with_support.shape[1] // 2

    def __compute_bounding_box(self):
        x_coords = [self.up_corner_sx[0], self.down_corner_sx[0], self.up_corner_dx[0], self.down_corner_dx[0]]
        y_coords = [self.up_corner_sx[1], self.down_corner_sx[1], self.up_corner_dx[1], self.down_corner_dx[1]]
        min_x, max_x = int(min(x_coords)), int(max(x_coords))
        min_y, max_y = int(min(y_coords)), int(max(y_coords))
        return min_x, max_x, min_y, max_y

    def __resize_matrix_if_needed(self, min_x, max_x, min_y, max_y):
        current_height, current_width = self.matrix_representation_with_support.shape
        required_width = max(max_x, current_width)
        required_height = max(max_y, current_height)

        if required_width > current_width or required_height > current_height:
            new_matrix = np.zeros((required_height, required_width), dtype=int)
            new_matrix[:current_height, :current_width] = self.matrix_representation_with_support
            self.matrix_representation_with_support = new_matrix

    def update_matrix_representation(self):
        support_size = Machine.SUCTION_CUPS_SUPPORT_DIMENSION.value
        # Rotate the corners
        self.__rotate_corners(math.radians(self.rotation_angle))

        # Compute the bounding box for the rotated suction cup
        min_x, max_x, min_y, max_y = self.__compute_bounding_box()

        # Resize the matrix if the bounding box exceeds current matrix dimensions
        self.__resize_matrix_if_needed(min_x, max_x, min_y, max_y)

        # Reset matrix (with support still intact)
        support_start_row = (self.matrix_representation_with_support.shape[0] - support_size) // 2
        support_start_col = (self.matrix_representation_with_support.shape[1] - support_size) // 2
        self.matrix_representation_with_support = np.zeros_like(self.matrix_representation_with_support)
        self.matrix_representation_with_support[support_start_row:support_start_row + support_size, support_start_col:support_start_col + support_size] = 1

        # Place the rotated suction cup inside the matrix
        for i in range(self.width):
            for j in range(self.height):
                x_rotated, y_rotated = self.__rotate_point(i, j, math.radians(self.rotation_angle))
                if (0 <= int(y_rotated) < self.matrix_representation_with_support.shape[0] and
                        0 <= int(x_rotated) < self.matrix_representation_with_support.shape[1]):
                    self.matrix_representation_with_support[int(y_rotated), int(x_rotated)] = 2

    def rotate(self, angle):
        self.rotation_angle += angle
        self.update_matrix_representation()

        return self.matrix_representation_with_support

    def get_matrix_representation_with_support(self):
        return np.array(self.matrix_representation_with_support)