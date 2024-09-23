import sys
import os
import time

sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('../../src'))
from src.utility.workpiece_drawer import WorkpieceDrawer
from src.model.workpiece_heat_map_model import WorkpieceHeatMapModel
from src.parameter.machine import Machine
import matplotlib.pyplot as plt


WORKPIECE_WIDTH = 2000
WORKPIECE_HEIGHT = 800

def get_workpiece_processing():
    workpiece_draw = WorkpieceDrawer(WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    workpiece_draw.draw_perimeter_piece()
    workpiece_draw.draw_rectangle_line((0, 0), (WORKPIECE_WIDTH - 1, WORKPIECE_HEIGHT - 1), 1)
    workpiece_draw.draw_rectangle_line((1300, 50), (1700, 300), 10)
    workpiece_draw.draw_circle_line((1000, 400), 200, 10)
    workpiece_draw.draw_circle_line((500, 200), 150, 10)
    workpiece_draw.draw_circle_line((1500, 600), 104, 10)

    return workpiece_draw.get_workpiece_processing_draw()


def compute_workpiece_heat_map(workpiece_processing):
    workpiece_model = WorkpieceHeatMapModel(workpiece_processing, WORKPIECE_WIDTH, WORKPIECE_HEIGHT, Machine.SUPPORT_AREA.value)
    print("Report first rectangle")
    workpiece_model.report_rectangle_piece((0, 0), (WORKPIECE_WIDTH - 1, WORKPIECE_HEIGHT - 1))
    print("Report second rectangle")
    workpiece_model.report_rectangle_piece((1300, 50), (1700, 300))
    print("Report first circle")
    workpiece_model.report_round_peace((1000, 400), 200)
    print("Report second circle")
    workpiece_model.report_round_peace((500, 200), 150)
    print("Report third circle")
    workpiece_model.report_round_peace((1500, 600), 104)

    return workpiece_model.compute_heat_map()

if __name__ == '__main__':
    start_time = time.time()
    print("Drawing piece....")
    workpiece_processing = get_workpiece_processing()
    duration = time.time() - start_time
    print("Drawing piece took: ", duration)
    print("Compute heat map....")
    start_time = time.time()
    workpiece_heat_map = compute_workpiece_heat_map(workpiece_processing)
    duration = time.time() - start_time
    print("Compute heat map took: ", duration)


    fig, axs = plt.subplots(1, 2, figsize=(10, 10))
    axs[0].imshow(workpiece_processing)
    axs[1].imshow(workpiece_heat_map)

    plt.show()
