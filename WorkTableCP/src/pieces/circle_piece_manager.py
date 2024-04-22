import numpy as np

class CirclePiece():

    def __init__(self, center, radius, heat_map, support_area):
        self.center_x, self.center_y = center
        self.radius = radius
        self.heat_map = heat_map
        self.support_area = support_area

    def __highlight_area_small_circle(self, distances, num_tiers):
        return num_tiers - np.floor(distances / (self.radius / num_tiers))

    def __highlight_area_big_circle(self, distances, num_tiers):
        return np.floor(distances / (self.radius / num_tiers)) + 1

    def highlight_area(self):
        Y, X = np.meshgrid(np.arange(self.heat_map.shape[0]), np.arange(self.heat_map.shape[1]))

        distances = np.sqrt((X - self.center_x) ** 2 + (Y - self.center_y) ** 2)
        distances = distances.T
        circle_area = np.pi * self.radius ** 2
        num_tiers = int(np.ceil(circle_area / self.support_area))

        if circle_area > self.support_area:
            if circle_area < self.support_area * 3:
                scores = self.__highlight_area_small_circle(distances, num_tiers)
            else:
                scores = self.__highlight_area_big_circle(distances, num_tiers)
            self.heat_map[distances <= self.radius] = scores[distances <= self.radius].astype(int)