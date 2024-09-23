import numpy as np

AREA_DISCRIMINATOR_SMALL = 1
AREA_DISCRIMINATOR_MIDDLE = 5
AREA_DISCRIMINATOR_BIG = 10

class CirclePiece:
    def __init__(self, center, radius, heat_map, support_area):
        self.center_x, self.center_y = center
        self.radius = radius
        self.circle_area = np.pi * radius ** 2
        self.heat_map = heat_map
        self.support_area = support_area

    def __compute_distances(self):
        """Compute distances from the center of the circle using vectorized NumPy."""
        Y, X = np.ogrid[:self.heat_map.shape[0], :self.heat_map.shape[1]]
        distances = np.sqrt((X - self.center_x) ** 2 + (Y - self.center_y) ** 2)
        return distances

    def __highlight_area_small_circle(self, max_score):
        """Generate scores for a small circle."""
        distances = self.__compute_distances()
        normalized_distances = distances / self.radius
        scores = (1 - normalized_distances) * max_score
        return np.clip(np.round(scores), 0, max_score).astype(int)

    def __highlight_area_middle_circle(self, max_score):
        """Generate scores for a middle-sized circle."""
        distances = self.__compute_distances()
        normalized_distances = distances / self.radius
        scores = normalized_distances * max_score
        return np.clip(np.round(scores), 0, max_score).astype(int)

    def __highlight_area_big_circle(self, max_score):
        """Generate scores for a large circle, considering both center and edge."""
        distances = self.__compute_distances()
        normalized_distances = distances / self.radius
        center_high_scores = (1 - normalized_distances) * max_score
        edge_high_scores = normalized_distances * max_score
        scores = np.maximum(center_high_scores, edge_high_scores)
        return np.clip(np.round(scores), 0, max_score).astype(int)

    def highlight_area(self, priority):
        """Highlight the heat map area based on the size of the circle."""
        ratio = round(self.circle_area / self.support_area)
        print(ratio)

        if ratio <= AREA_DISCRIMINATOR_SMALL:
            print("Circle is too small")
            return self.heat_map

        # Determine the type of scoring based on the area ratio
        if ratio < AREA_DISCRIMINATOR_MIDDLE:
            print("Small circle")
            scores = self.__highlight_area_small_circle(AREA_DISCRIMINATOR_SMALL * priority)
        elif ratio < AREA_DISCRIMINATOR_BIG:
            print("Medium circle")
            scores = self.__highlight_area_middle_circle(AREA_DISCRIMINATOR_MIDDLE * priority)
        else:
            print("Large circle")
            scores = self.__highlight_area_big_circle(AREA_DISCRIMINATOR_BIG * priority)

        # Apply scores only to points inside the circle
        distances = self.__compute_distances()
        mask = distances <= self.radius
        self.heat_map[mask] += scores[mask]

        return self.heat_map
