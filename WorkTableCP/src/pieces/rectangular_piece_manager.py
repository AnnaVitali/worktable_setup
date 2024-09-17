import numpy as np
import sympy
from sympy import Polygon
from skimage import draw

AREA_DISCRIMINATOR = 3
AREA_INCREMENT = 2
EPSILON = 1e-6

class RectangularPiece:

    def __init__(self, up_left_vertex, down_right_vertex, heat_map, support_area):
        self.start_x, self.start_y = up_left_vertex
        self.end_x, self.end_y = down_right_vertex
        self.heat_map = heat_map
        self.width = self.end_x - self.start_x
        self.height = self.end_y - self.start_y
        self.support_area = support_area
        self.side_support_area = round(np.sqrt(self.support_area))
        self.rectangle = self.__instantiate_rectangle()
        self.rectangle_area = self.rectangle.area.evalf()
        self.__compute_center_coordinate()

    def __compute_center_coordinate(self):
        centroid_x, centroid_y = self.rectangle.centroid.coordinates
        self.centroid_x = float(round(centroid_x.evalf()))
        self.centroid_y = float(round(centroid_y.evalf()))
        print(self.centroid_x)
        print(self.centroid_y)

    def __instantiate_rectangle(self):
        return Polygon((self.start_x, self.start_y), (self.end_x, self.start_y), (self.end_x, self.end_y),
                       (self.start_x, self.end_y))

    def __compute_distances(self):
        Y, X = np.ogrid[:self.height, :self.width]
        distances = np.sqrt((X - self.centroid_x) ** 2 + (Y - self.centroid_y) ** 2)
        return distances

    def __highlight_area_small_rectangle(self):
        distances = self.__compute_distances()
        normalized_distances = distances / (np.max(distances) + EPSILON)
        max_score = self.rectangle_area / self.support_area
        scores = (1 - normalized_distances) * max_score
        return np.round(scores).astype(int)

    def __highlight_area_middle_rectangle(self):
        print("compute distance")
        distances = self.__compute_distances()
        print("normalized distances")
        normalized_distances = distances / np.max(distances)
        normalized_distances = np.array(normalized_distances)
        print(np.any(np.isnan(normalized_distances)))
        print(np.any(np.isinf(normalized_distances)))
        print("compute score")
        max_score = self.rectangle_area / self.support_area
        print(max_score)
        print(normalized_distances.shape)
        scores = normalized_distances * max_score
        print("score computed")
        return np.round(scores).astype(int)

    def __highlight_area_big_rectangle(self):
        distances = self.__compute_distances()
        normalized_distances = distances / np.max(distances)
        normalized_distances = np.array(normalized_distances)
        max_score = self.rectangle_area / self.support_area
        center_high_scores = (1 - normalized_distances) * max_score
        edge_high_scores = normalized_distances * max_score
        scores = np.maximum(center_high_scores, edge_high_scores)
        return np.round(scores).astype(int)

    def highlight_area(self):
        if self.rectangle_area < self.support_area:
            return

        if self.rectangle_area < self.support_area * AREA_DISCRIMINATOR:
            print("is small")
            scores = self.__highlight_area_small_rectangle()
        elif self.rectangle_area >= self.support_area * AREA_DISCRIMINATOR:
            print("is middle")
            scores = self.__highlight_area_middle_rectangle()
        else:
            print("is big")
            scores = self.__highlight_area_big_rectangle()

        self.heat_map[self.start_y:self.end_y, self.start_x:self.end_x] += scores