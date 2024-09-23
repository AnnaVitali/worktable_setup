import numpy as np

AREA_DISCRIMINATOR_SMALL = 2
AREA_DISCRIMINATOR_MIDDLE = 5
AREA_DISCRIMINATOR_BIG = 20

class RectangularPiece:
    def __init__(self, up_left_vertex, down_right_vertex, heat_map, support_area):
        # Set start and end points of the rectangle
        self.start_x, self.start_y = up_left_vertex
        self.end_x, self.end_y = down_right_vertex

        # Heat map and dimensions
        self.heat_map = heat_map
        self.width = self.end_x - self.start_x
        self.height = self.end_y - self.start_y

        # Support area and derived side length
        self.support_area = support_area
        self.side_support_area = round(np.sqrt(self.support_area))

        # Directly compute rectangle area and centroid (no need for SymPy)
        self.rectangle_area = self.width * self.height
        self.centroid_x = (self.start_x + self.end_x) / 2
        self.centroid_y = (self.start_y + self.end_y) / 2

    def __compute_distances(self):
        """Compute normalized distances from the center of the rectangle to the edges."""
        # Create a grid of Y and X coordinates
        Y, X = np.ogrid[:self.height, :self.width]

        # Compute relative distances from the center (centroid)
        center_y = self.centroid_y - self.start_y
        center_x = self.centroid_x - self.start_x

        # Aspect ratio handling for scaling
        aspect_ratio = self.width / self.height
        distances_y = np.abs(Y - center_y) / self.height
        distances_x = np.abs(X - center_x) / self.width

        # Compute Euclidean distance from the center, adjusted for aspect ratio
        distances = np.sqrt(distances_y**2 + (distances_x / aspect_ratio)**2)

        # Normalize distances between 0 and 1
        normalized_distances = distances / np.max(distances)
        return normalized_distances

    def __highlight_area_small_rectangle(self, max_score):
        """Highlight small rectangle area based on distance to center."""
        normalized_distances = self.__compute_distances()
        scores = (1 - normalized_distances) * max_score
        return np.clip(np.round(scores), 0, max_score).astype(int)

    def __highlight_area_middle_rectangle(self, max_score):
        """Highlight middle rectangle area based on distance to edges."""
        normalized_distances = self.__compute_distances()
        scores = normalized_distances * max_score
        return np.clip(np.round(scores), 0, max_score).astype(int)

    def __highlight_area_big_rectangle(self, max_score):
        """Highlight large rectangle area with scores biased toward both center and edges."""
        normalized_distances = self.__compute_distances()
        center_high_scores = (1 - normalized_distances) * max_score
        edge_high_scores = normalized_distances * max_score
        scores = np.maximum(center_high_scores, edge_high_scores)
        return np.clip(np.round(scores), 0, max_score).astype(int)

    def highlight_area(self, priority):
        """Highlight the heat map area based on the size of the rectangle."""
        # Compute the ratio of rectangle area to support area
        ratio = round(self.rectangle_area / self.support_area)

        # Depending on the size of the rectangle, choose the appropriate scoring method
        if ratio <= AREA_DISCRIMINATOR_SMALL:
            return self.heat_map

        if ratio < AREA_DISCRIMINATOR_MIDDLE:
            print("Small rectangle")
            scores = self.__highlight_area_small_rectangle(AREA_DISCRIMINATOR_SMALL * priority)
        elif ratio < AREA_DISCRIMINATOR_BIG:
            print("Middle rectangle")
            scores = self.__highlight_area_middle_rectangle(AREA_DISCRIMINATOR_MIDDLE * priority)
        else:
            print("Large rectangle")
            scores = self.__highlight_area_big_rectangle(AREA_DISCRIMINATOR_BIG * priority)

        # Add the computed scores to the heat map
        self.heat_map[self.start_y:self.end_y, self.start_x:self.end_x] += scores

        return self.heat_map
