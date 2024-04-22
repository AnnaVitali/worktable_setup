import numpy as np

class CircleDrawer():

    def draw_circle(self, center, radius, matrix, value, thickness = 1):
        x, y = center
        for r in range(matrix.shape[0]):
            for c in range(matrix.shape[1]):
                distance = np.sqrt((r - y) ** 2 + (c - x) ** 2)
                if radius <= distance <= radius + thickness:
                    matrix[r, c] = value