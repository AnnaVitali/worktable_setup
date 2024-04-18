from sympy import Point2D, Polygon

if __name__ == '__main__':
    points = (Point2D(665, 394), Point2D(20, 135), Point2D(665, 4), Point2D(689, 17),
              Point2D(689, 380), Point2D(665, 394))
    sides = [((665, 394), (20, 262)), ((20, 262), (20, 135)), ((20, 135), (665, 4)), ((665, 4), (689, 17)),
             ((689, 17), (689, 380)), ((689, 380), (665, 394))]

    polygon = Polygon(*points)



    # fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    # axs[0].imshow(workpiece_processing)
    # axs[1].imshow(workpiece_heat_map)
    #
    # plt.show()