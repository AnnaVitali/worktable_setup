import sympy
import numpy as np
import matplotlib.pyplot as plt
from sympy import Point2D, Polygon

if __name__ == '__main__':
    points = (Point2D(665, 394), Point2D(20, 262), Point2D(20, 135), Point2D(665, 4), Point2D(689, 17),
              Point2D(689, 380), Point2D(665, 394))
    sides = [((665, 394), (20, 262)), ((20, 262), (20, 135)), ((20, 135), (665, 4)), ((665, 4), (689, 17)),
             ((689, 17), (689, 380)), ((689, 380), (665, 394))]

    polygon = Polygon(*points)

    centroid_x, centroid_y = polygon.centroid.coordinates
    centroid_x = round(centroid_x.evalf())
    centroid_y = round(centroid_y.evalf())

    jx, jy, jxy = polygon.second_moment_of_area()
    alpha_x = sympy.atan2(2 * jxy, jx - jy) / 2

    print(alpha_x.evalf())

    m_x = sympy.tan(alpha_x)
    m_y = - 1/ m_x
    q_x = centroid_y - m_x * centroid_x
    q_y = -m_y * centroid_x + centroid_y



    print(f'alpha: {alpha_x.evalf()}, m: {m_x.evalf()}, q: {q_x.evalf()}')

    x = np.linspace(min([float(point.x) for point in points]), max([float(point.x) for point in points]), 400)

    # Calculate the corresponding y values
    line_x = m_x * x + q_x
    line_y = m_y * x + q_y

    # Create the plot
    plt.figure()

    # Draw the line
    plt.plot(x, line_x, label=f'inertia_axis')
    plt.plot(x, line_y, label=f'inertia_axis')

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