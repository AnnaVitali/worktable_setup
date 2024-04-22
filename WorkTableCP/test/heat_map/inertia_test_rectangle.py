import sympy
import numpy as np
import matplotlib.pyplot as plt
from sympy import Point2D, Polygon

WORKPIECE_WIDTH = 2000
WORKPIECE_HEIGHT = 800

if __name__ == '__main__':
    start_x, start_y = (0, 0)
    end_x, end_y = (WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    points = (Point2D(start_x, start_y), Point2D(end_x, start_y), Point2D(end_x, end_y), Point2D(start_x, end_y))
    polygon = Polygon(*points)
    centroid_x, centroid_y = polygon.centroid.coordinates
    # For the vertical line: x = center_x
    # For the horizontal line: y = center_y
    centroid_x = round(centroid_x.evalf())
    centroid_y = round(centroid_y.evalf())

    start_x, start_y = (0, 0)
    end_x, end_y = (WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    # Create the plot
    plt.figure()

    # Draw the vertical symmetry axis
    plt.plot([centroid_x, centroid_x], [start_y, end_y], label='Vertical symmetry axis')

    # Draw the horizontal symmetry axis
    plt.plot([start_x, end_x], [centroid_y, centroid_y], label='Horizontal symmetry axis')

    # Plot the centroid point
    plt.scatter(centroid_x, centroid_y, color='red')

    # Plot the polygon
    x_coords, y_coords = zip(*[(point.x, point.y) for point in points])
    plt.fill(x_coords, y_coords, 'b', alpha=0.3)  # Plot the polygon with a blue color and 30% transparency

    # Set the title and labels
    plt.title('Line Plot')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.xlim(min([float(point.x) for point in points]), max([float(point.x) for point in points]))
    plt.ylim(min([float(point.y) for point in points]), max([float(point.y) for point in points]))

    # Show the plot
    plt.show()
    # fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    # axs[0].imshow(workpiece_processing)
    # axs[1].imshow(workpiece_heat_map)
    #
    # plt.show()