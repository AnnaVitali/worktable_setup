from utility.workpiece_designer import WorkpieceDesigner
from model.workpiece_model import WorkpieceModel
import numpy as np
import matplotlib.pyplot as plt


WORKPIECE_WIDTH = 2000
WORKPIECE_HEIGHT = 800
AVAILABLE_BARS = 8
BAR_SIZE = 145
SECURITY_DISTANCE_BARS = 200
AVAILABLE_SUCTIONS_CUPS = 24
SUCTION_CUPS_SIZE = 145
SECURITY_DISTANCE_SUCTION_CUPS = 145
SUPPORT_AREA = 145 ** 2

def get_workpiece_processing():
    workpiece_draw = WorkpieceDesigner(WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    workpiece_draw.draw_perimeter_piece()
    workpiece_draw.draw_rectangle_line((0, 0), (WORKPIECE_WIDTH - 1, WORKPIECE_HEIGHT - 1), 1)
    workpiece_draw.draw_rectangle_line((1300, 50), (1700, 300), 10)
    workpiece_draw.draw_circle_line((1000, 400), 200, 10)
    workpiece_draw.draw_circle_line((500, 200), 150, 10)
    workpiece_draw.draw_circle_line((1500, 600), 104, 10)

    return workpiece_draw.get_workpiece_processing_draw()


def compute_workpiece_heat_map(workpiece_processing):
    workpiece_model = WorkpieceModel(workpiece_processing, WORKPIECE_WIDTH, WORKPIECE_HEIGHT, SUPPORT_AREA)
    workpiece_model.report_rectangle_piece((0, 0), (WORKPIECE_WIDTH - 1, WORKPIECE_HEIGHT - 1))
    workpiece_model.report_rectangle_piece((1300, 50), (1700, 300))
    workpiece_model.report_round_peace((1000, 400), 200)
    workpiece_model.report_round_peace((500, 200), 150)
    workpiece_model.report_round_peace((1500, 600), 104)

    return workpiece_model.compute_heat_map()

if __name__ == '__main__':
    workpiece_processing = get_workpiece_processing()
    workpiece_heat_map = compute_workpiece_heat_map(workpiece_processing)


    fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    axs[0].imshow(workpiece_processing)
    axs[1].imshow(workpiece_heat_map)

    plt.show()
