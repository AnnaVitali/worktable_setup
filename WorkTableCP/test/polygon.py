import sys
import os
from sympy import Point2D

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
from src.utility.workpiece_designer import WorkpieceDesigner
from src.model.workpiece_model import WorkpieceModel
import matplotlib.pyplot as plt

WORKPIECE_WIDTH = 715
WORKPIECE_HEIGHT = 400
SUPPORT_AREA = 145 ** 2



def get_workpiece_processing(sides):
    workpiece_draw = WorkpieceDesigner(WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    workpiece_draw.draw_perimeter_piece()

    contouring_thickness = 20

    workpiece_draw.draw_thick_line(sides[0][0], sides[0][1], contouring_thickness, "up")
    workpiece_draw.draw_thick_line(sides[1][0], sides[1][1], contouring_thickness, "left")
    workpiece_draw.draw_thick_line(sides[2][0], sides[2][1], contouring_thickness, "down")
    workpiece_draw.draw_thick_line(sides[3][0], sides[3][1], contouring_thickness, "right")
    workpiece_draw.draw_thick_line(sides[4][0], sides[4][1], contouring_thickness, "right")
    workpiece_draw.draw_thick_line(sides[5][0], sides[5][1], contouring_thickness, "right")


    return workpiece_draw.get_workpiece_processing_draw()

def compute_workpiece_heat_map(workpiece_processing, sides):
    workpiece_model = WorkpieceModel(workpiece_processing, WORKPIECE_WIDTH, WORKPIECE_HEIGHT, SUPPORT_AREA)
    points = (Point2D(665, 394), Point2D(20, 135), Point2D(665, 4), Point2D(689, 17),
              Point2D(689, 380), Point2D(665, 394))
    workpiece_model.report_polygonal_piece(points, sides)

    return workpiece_model.compute_heat_map()

if __name__ == '__main__':
    sides = [((665, 394), (20, 262)), ((20, 262), (20, 135)), ((20, 135), (665, 4)), ((665, 4), (689, 17)),
             ((689, 17), (689, 380)), ((689, 380), (665, 394))]

    workpiece_processing = get_workpiece_processing(sides)
    workpiece_heat_map = compute_workpiece_heat_map(workpiece_processing, sides)

    fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    axs[0].imshow(workpiece_processing)
    axs[1].imshow(workpiece_heat_map)

    plt.show()
