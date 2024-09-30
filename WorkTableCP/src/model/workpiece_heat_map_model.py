import numpy as np
from pieces.polygonal_piece_manager import PolygonalPiece
from pieces.rectangular_piece_manager import RectangularPiece
from pieces.circle_piece_manager import CirclePiece
from parameter.workings import Workings

INCREMENT_IMPORTANCE = 1
MAXIMUM_IMPORTANCE = 2

class WorkpieceHeatMapModel:
    def __init__(self, workpiece_processing, workpiece_width, workpiece_height, support_area):
        self.workpiece_processing = workpiece_processing
        self.workpiece_width = workpiece_width
        self.workpiece_height = workpiece_height
        self.support_area = support_area
        self.heat_map = np.zeros((workpiece_height, workpiece_width), dtype=int)

    def __highlight_pass_through_workings(self):
        """Efficiently highlight pass-through working points."""
        pass_through_mask = self.workpiece_processing == Workings.PASS_THROUGH_WORKING_POINT.value

        # Update the heatmap where pass-through points exist
        self.heat_map[pass_through_mask] = self.workpiece_processing[pass_through_mask]

        # Efficient vectorized approach to check neighboring cells
        offsets = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])  # Up, Down, Left, Right

        pass_through_points = np.argwhere(pass_through_mask)
        for point in pass_through_points:
            neighbors = point + offsets
            valid_neighbors = ((0 <= neighbors[:, 0]) & (neighbors[:, 0] < self.workpiece_height) &
                               (0 <= neighbors[:, 1]) & (neighbors[:, 1] < self.workpiece_width))

            # Filter out valid neighbors
            for ni, nj in neighbors[valid_neighbors]:
                if (self.workpiece_processing[ni, nj] != Workings.PASS_THROUGH_WORKING_POINT.value and
                        self.workpiece_processing[ni, nj] <= MAXIMUM_IMPORTANCE):
                    self.heat_map[ni, nj] = min(self.heat_map[ni, nj] + INCREMENT_IMPORTANCE, MAXIMUM_IMPORTANCE)

    def __compute_distance(self, point1, point2):
        """Compute Euclidean distance between two points."""
        return np.linalg.norm(np.array(point1) - np.array(point2))

    def report_polygonal_piece(self, points, sides, priority=1):
        """Report a polygonal piece and update the heat map."""
        polygonal_piece = PolygonalPiece(points, sides, self.heat_map, self.support_area)
        polygonal_piece.highlight_area(priority)

    def report_rectangle_piece(self, start_coordinates, end_coordinates, priority=1):
        """Report a rectangular piece and update the heat map."""
        rectangular_piece = RectangularPiece(start_coordinates, end_coordinates, self.heat_map, self.support_area)
        self.heat_map = rectangular_piece.highlight_area(priority)

    def report_round_peace(self, center_coordinates, radius, priority=1):
        """Report a circular piece and update the heat map."""
        circle_piece = CirclePiece(center_coordinates, radius, self.heat_map, self.support_area)
        self.heat_map = circle_piece.highlight_area(priority)

    def compute_heat_map(self):
        """Compute the heat map by highlighting pass-through workings and other pieces."""
        self.__highlight_pass_through_workings()
        return self.heat_map
