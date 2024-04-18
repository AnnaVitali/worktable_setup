import sys
import os
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
from src.utility.workpiece_drawer import WorkpieceDrawer
from src.model.workpiece_heat_map_model import WorkpieceHeatMapModel
from src.model.bar_model import BarModel
from src.model.suction_cup_model import SuctionCupModel
from src.parameter.machine import Machine
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait


WORKPIECE_WIDTH = 2000
WORKPIECE_HEIGHT = 800

def get_workpiece_processing():
    workpiece_draw = WorkpieceDrawer(WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    workpiece_draw.draw_perimeter_piece()
    workpiece_draw.draw_rectangle_line((0, 0), (WORKPIECE_WIDTH - 1, WORKPIECE_HEIGHT - 1),
                                       1)

    return workpiece_draw.get_workpiece_processing_draw()


def compute_workpiece_heat_map(workpiece_processing):
    workpiece_model = WorkpieceHeatMapModel(workpiece_processing, WORKPIECE_WIDTH, WORKPIECE_HEIGHT, Machine.SUPPORT_AREA.value)
    workpiece_model.report_rectangle_piece((0, 0), (WORKPIECE_WIDTH, WORKPIECE_HEIGHT))
    return workpiece_model.compute_heat_map()

def compute_bars_location(workpiece_heat_map):
    bar_model = BarModel(workpiece_heat_map, WORKPIECE_WIDTH, Machine.AVAILABLE_BARS, Machine.BAR_SIZE,
                         Machine.SECURITY_DISTANCE_BARS.value)
    bars_location = bar_model.compute_bar_location()
    return bar_model, bars_location

def compute_suction_cup_location(workpiece_heat_map, bar_used, bars_location):
    suction_cups_image = np.zeros(np.array(workpiece_processing).shape)
    suction_cups_locators = []
    results = []
    columns = []

    i = 0
    n_threads = bar_used
    with ThreadPoolExecutor(n_threads) as executor:
        for column in bars_location:
            heat_map_bar = np.array(workpiece_heat_map)[:, column: column + Machine.BAR_SIZE]
            suction_cups_locators.append(SuctionCupModel(heat_map_bar, WORKPIECE_HEIGHT, Machine.AVAILABLE_SUCTIONS_CUPS.value,
                                                         Machine.BAR_SIZE.value, Machine.SUCTION_CUPS_SIZE.value,
                                                         Machine.SECURITY_DISTANCE_SUCTION_CUPS.value))
            results.append(
                executor.submit(suction_cups_locators[i].compute_suction_cups_location()))
            columns.append(column)
            i += 1

        wait(results)

        for index, column in enumerate(np.array(columns)):
            suction_cups_image += suction_cups_locators[index].get_suction_cup_position_image(
             np.array(workpiece_processing).shape, column)
    return suction_cups_locators, suction_cups_image

if __name__ == '__main__':
    workpiece_processing = get_workpiece_processing()
    workpiece_heat_map = compute_workpiece_heat_map(workpiece_processing)
    bar_model, bars_location = compute_bars_location(workpiece_heat_map)
    print(bars_location)
    bar_used = bar_model.get_num_bars_used()
    bars_image = bar_model.get_bar_position_image()
    suction_cups_locators, suction_cups_image = compute_suction_cup_location(workpiece_heat_map, bar_used, bars_location)

    fig, axs = plt.subplots(1, 3, figsize=(10, 10))
    axs[0].imshow(workpiece_heat_map)
    axs[1].imshow(workpiece_processing + bars_image)
    axs[2].imshow(workpiece_processing + bars_image+ suction_cups_image)

    plt.show()
