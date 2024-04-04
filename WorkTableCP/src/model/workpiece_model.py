import numpy as np
from skimage import draw

PASS_THROUGH_WORKING_POINT = -1
PERIMETER_POINT = 1
FIGURE_AXIS = 3
INCREMENT_IMPORTANCE = 1
MAXIMUM_IMPORTANCE = 2


class WorkpieceModel():

    def __init__(self, workpiece_processing, workpiece_width, workpiece_height, support_area):
        self.workpiece_processing = workpiece_processing
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.support_area = support_area
        self.heat_map_model = np.zeros((workpiece_height, workpiece_width), dtype=int)

    def __highlight_perimeter(self):
        for i in range(self.workpiece_height):
            for j in range(self.workpiece_width):
                if self.workpiece_processing[i, j] == PERIMETER_POINT:
                    self.heat_map_model[i, j] += INCREMENT_IMPORTANCE

    def __highlight_pass_through_workings(self):
        self.heat_map_model = np.where(self.workpiece_processing == -1, self.workpiece_processing, self.heat_map_model)
        point_checked = []
        for i in range(self.workpiece_height):
            for j in range(self.workpiece_width):
                if self.workpiece_processing[i, j] == PASS_THROUGH_WORKING_POINT:
                    for r, c in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if ((0 <= i + r < self.workpiece_height) and (0 <= j + c < self.workpiece_width)
                                and not point_checked.__contains__((i + r, j + c))
                                and self.workpiece_processing[i + r, j + c] != PASS_THROUGH_WORKING_POINT
                                and self.workpiece_processing[i + r, j + c] <= MAXIMUM_IMPORTANCE):
                            self.heat_map_model[i + r, j + c] = min(
                                self.heat_map_model[i + r, j + c] + INCREMENT_IMPORTANCE, MAXIMUM_IMPORTANCE)
                            point_checked.append((i + r, j + c))

    def report_polygonal_piece(self, start_vertex_coordinates, end_vertex_coordinates):
        rr, cc = draw.polygon(end_vertex_coordinates, start_vertex_coordinates, shape=self.heat_map_model.shape)
        self.heat_map_model[rr, cc] = np.where(self.workpiece_processing[rr, cc] != PASS_THROUGH_WORKING_POINT,
                                               self.heat_map_model[rr, cc] + INCREMENT_IMPORTANCE,
                                               self.heat_map_model[rr, cc])

    def report_rectangle_piece(self, start_coordinates, end_coordinates):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates
        side_support_area = int(np.sqrt(self.support_area))

        width = end_x - start_x
        height = end_y - start_y

        num_tiers = round((min(width, height) / 2) / side_support_area)

        print(f"num tires: {num_tiers}")

        scores = np.zeros((height, width), dtype=int)
        min_x = 0
        min_y = 0
        max_x = width
        max_y = height

        if(int(height / 2) - side_support_area < 0):
            for i in range(1, num_tiers + 1):
                if(min_x <= max_x and min_y <= max_y):
                    scores[min_y:max_y, min_x: min_x + side_support_area] = i
                    scores[min_y:max_y, max_x - side_support_area: max_x] = i
                    scores[min_y: min_y + side_support_area, min_x:max_x] = i
                    scores[max_y - side_support_area:max_y, min_x:max_x] = i

                    min_x += side_support_area
                    min_y += side_support_area
                    max_x -= side_support_area
                    max_y -= side_support_area
        else:
            offset = int(side_support_area / 2)#the side of the square should be as long as thes support
            min_center_x = int(width / 2) - offset
            min_center_y = int(height / 2) - offset
            max_center_x = int(width / 2) + offset
            max_center_y = int(height / 2) + offset

            for i in range(num_tiers, 0, -1):
                print(f"inner min:{min_center_x}, {min_center_y}")
                print(f"outer min:{min_x}, {min_y}")
                print(f"inner max:{max_center_x}, {max_center_y}")
                print(f"outer max:{max_x}, {max_y}")
                if(min_center_y > min_y and min_center_x > min_x and max_center_y < max_y and max_center_x < max_x ):
                    scores[min_center_y: max_center_y, min_center_x: min_center_x + offset] = i
                    scores[min_center_y: max_center_y, max_center_x - offset: max_center_x] = i
                    scores[min_center_y: min_center_y + offset, min_center_x:max_center_x] = i
                    scores[max_center_y - offset:max_center_y, min_center_x:max_center_x] = i

                    scores[min_y:max_y, min_x: min_x + side_support_area] = i
                    scores[min_y:max_y, max_x - side_support_area: max_x] = i
                    scores[min_y: min_y + side_support_area, min_x:max_x] = i
                    scores[max_y - side_support_area:max_y, min_x:max_x] = i

                    min_center_x -= offset
                    min_center_y -= offset
                    max_center_x += offset
                    max_center_y += offset

                    min_x += side_support_area
                    min_y += side_support_area
                    max_x -= side_support_area
                    max_y -= side_support_area

        self.heat_map_model[start_y:end_y, start_x:end_x] = scores


    def report_round_peace(self, center_coordinates, radius):
        center_x, center_y = center_coordinates
        Y, X  = np.meshgrid(np.arange(self.heat_map_model.shape[0]), np.arange(self.heat_map_model.shape[1]))

        distances = np.sqrt((X - center_x) ** 2 + (Y - center_y) ** 2)
        distances = distances.T
        circle_area = np.pi * radius ** 2

        print(f"circle area: {circle_area}, support area: {self.support_area}")
        num_tiers = int(np.ceil(circle_area / self.support_area))

        if circle_area > self.support_area:
            if circle_area < self.support_area * 3:
                scores = num_tiers - np.floor(distances / (radius /num_tiers))
            else:
                scores = np.floor(distances / (radius / num_tiers)) + 1

            self.heat_map_model[distances <= radius] = scores[distances <= radius].astype(int)


    def compute_heat_map(self):
        self.__highlight_perimeter()
        self.__highlight_pass_through_workings()
        return self.heat_map_model
