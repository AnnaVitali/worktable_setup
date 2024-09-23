import numpy as np
import sympy
from sympy import Polygon, Point
from skimage import draw

INCREMENT_VALUE = 2
AREA_VALUE = 1
CENTROID_VALUE = 4
PASS_THROUGH_WORKING = -1

AREA_DISCRIMINATOR_SMALL = 2
AREA_DISCRIMINATOR_MIDDLE = 5
AREA_DISCRIMINATOR_BIG = 20

class PolygonalPiece():

    def __init__(self, points, sides, workpiece_processing, support_area):
        self.points = points
        self.sides = sides
        self.support_area = support_area
        self.heat_map = workpiece_processing
        self.polygon_heat_map = np.zeros_like(self.heat_map)
        self.polygon = self.__instantiate_polygon()
        self.polygon_area = float(self.polygon.area.evalf())

    def __instantiate_polygon(self):
        return Polygon(*self.points)

    def __compute_mid_points(self):
        mid_points = []
        for index, side in enumerate(self.sides):
            start, end = side
            start_x, start_y = start
            end_x, end_y = end
            mid_x = round((end_x + start_x) / 2)
            mid_y = round((end_y + start_y) / 2)
            mid_points.append((mid_x, mid_y))
        return mid_points

    def __compute_inertia_axis(self):
        jx, jy, jxy = self.polygon.second_moment_of_area()
        centroid_x, centroid_y = self.polygon.centroid.coordinates
        alpha_x = sympy.atan2(2 * jxy, jx - jy) / 2
        m_x = sympy.tan(alpha_x)
        m_y = - 1 / m_x
        q_x = centroid_y - m_x * centroid_x
        q_y = -m_y * centroid_x + centroid_y
        return float(m_x.evalf()), float(m_y.evalf()), float(q_x.evalf()), float(q_y.evalf())

    def __draw_simple_line(self, start_coordinates, end_coordinates):
        start_x, start_y = start_coordinates
        end_x, end_y = end_coordinates

        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)

        sx = -1 if start_x > end_x else 1
        sy = -1 if start_y > end_y else 1

        x, y = start_x, start_y
        self.heat_map[y][x] += INCREMENT_VALUE

        if dx > dy:
            err = dx / 2.0
            while x != end_x:
                self.heat_map[y][x] += INCREMENT_VALUE
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != end_y:
                self.heat_map[y][x] += INCREMENT_VALUE
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy

    def __compute_distance_between_point_and_line(self, point, m, q):
        return int(abs(m * point[0] - point[1] + q) / np.sqrt(m ** 2 + 1))

    def __compute_distances(self):
        """Compute distances within the polygon area using NumPy for speed and SymPy for polygon representation."""
        # Get the x and y coordinates of the polygon's vertices
        x_cords = [float(point.x) for point in self.polygon.vertices]
        y_cords = [float(point.y) for point in self.polygon.vertices]

        # Get the centroid of the polygon (SymPy handles this)
        centroid = self.polygon.centroid
        centroid_x, centroid_y = float(centroid.x), float(centroid.y)

        # Get the mask of points inside the polygon using skimage's draw.polygon
        rr, cc = draw.polygon(y_cords, x_cords, self.heat_map.shape)
        mask = np.zeros_like(self.heat_map, dtype=bool)
        mask[rr, cc] = True

        # Prepare distance array
        combined_distances = np.zeros_like(self.heat_map, dtype=float)

        # Vectorized centroid distance calculation (NumPy)
        Y, X = np.ogrid[:self.heat_map.shape[0], :self.heat_map.shape[1]]
        centroid_distances = np.sqrt((X - centroid_x) ** 2 + (Y - centroid_y) ** 2)

        # Edge distance calculation using NumPy
        edge_distances = np.full(centroid_distances.shape, np.inf)

        # Loop through each edge (pair of consecutive vertices) to compute distances
        for i in range(len(self.polygon.vertices)):
            p1 = np.array([x_cords[i], y_cords[i]])  # First vertex of the edge
            p2 = np.array([x_cords[(i + 1) % len(self.polygon.vertices)],
                           y_cords[(i + 1) % len(self.polygon.vertices)]])  # Next vertex (with wrap-around)

            # Vectorized perpendicular distance to the line segment between p1 and p2
            A = p1[1] - p2[1]  # y1 - y2
            B = p2[0] - p1[0]  # x2 - x1
            C = p1[0] * p2[1] - p2[0] * p1[1]  # x1*y2 - x2*y1

            # Compute perpendicular distance from each point (X, Y) to the line Ax + By + C = 0
            distance_to_edge = np.abs(A * X + B * Y + C) / np.sqrt(A ** 2 + B ** 2)

            # Update minimum edge distances
            edge_distances = np.minimum(edge_distances, distance_to_edge)

        # For each masked point, take the minimum of centroid and edge distances
        combined_distances[mask] = np.minimum(centroid_distances[mask], edge_distances[mask])

        # Normalize distances (0 = closest to center or edge, 1 = farthest)
        max_distance = np.max(combined_distances[mask])
        normalized_distances = combined_distances / max_distance
        normalized_distances *= mask  # Apply mask to restrict to polygon area

        return normalized_distances, rr, cc

    def __highlight_area_small_polygon(self, max_score):
        normalized_distances, rr, cc = self.__compute_distances()
        scores = (1 - normalized_distances[rr, cc]) * max_score
        scores = np.clip(scores, 0, max_score)
        self.heat_map[rr, cc] += np.round(scores).astype(int)

    def __highlight_area_middle_polygon(self, max_score):
        normalized_distances, rr, cc = self.__compute_distances()
        scores = normalized_distances[rr, cc] * max_score
        scores = np.clip(scores, 0, max_score)
        self.heat_map[rr, cc] += np.round(scores).astype(int)

    def __highlight_area_big_polygon(self, max_score):
        normalized_distances, rr, cc = self.__compute_distances()
        scores = (1 - normalized_distances[rr, cc]) * max_score
        scores = np.clip(scores, 0, max_score)
        self.polygon_heat_map[rr, cc] += np.round(scores).astype(int)

    def highlight_area(self, priority):
        self.polygon_area = self.polygon.area.evalf()
        ratio = self.polygon_area / self.support_area

        if ratio <= AREA_DISCRIMINATOR_SMALL:
            return self.heat_map

        if ratio < AREA_DISCRIMINATOR_MIDDLE:
            print("is small")
            self.__highlight_area_small_polygon(AREA_DISCRIMINATOR_SMALL * priority)
        elif ratio < AREA_DISCRIMINATOR_BIG:
            print("is middle")
            self.__highlight_area_middle_polygon(AREA_DISCRIMINATOR_MIDDLE * priority)
            print("heat_map computed")
        else:
            print("is big")
            self.__highlight_area_big_polygon(AREA_DISCRIMINATOR_BIG * priority)