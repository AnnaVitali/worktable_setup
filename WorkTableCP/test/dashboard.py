import subprocess
from utility.workpiece_designer import WorkpieceDesigner
from model.workpiece_model import WorkpieceModel
from model.bar_model import BarModel
from model.suction_cup_model import SuctionCupModel
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait

WORKPIECE_WIDTH = 1000
WORKPIECE_HEIGHT = 800
AVAILABLE_BARS = 8
BAR_SIZE = 145
SECURITY_DISTANCE_BARS = 110
AVAILABLE_SUCTIONS_CUPS = 24
SUCTION_CUPS_SIZE = 145
SECURITY_DISTANCE_SUCTION_CUPS = 40
SUPPORT_AREA = 145 ** 2

def get_workpiece_processing():
    workpiece_draw = WorkpieceDesigner(WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    workpiece_draw.draw_perimeter_piece()
    workpiece_draw.draw_rectangle_line((42, 177), (936, 600), 20)

    workpiece_draw.draw_circle_line((206, 394), 139, 12)
    workpiece_draw.draw_circle_line((500, 394), 104, 12)
    workpiece_draw.draw_circle_line((700, 438), 17, 12)
    workpiece_draw.draw_circle_line((700, 366), 17, 12)
    workpiece_draw.draw_circle_line((700, 288), 19, 12)

    return workpiece_draw.get_workpiece_processing_draw()


def compute_workpiece_heat_map(workpiece_processing):
    workpiece_model = WorkpieceModel(workpiece_processing, WORKPIECE_WIDTH, WORKPIECE_HEIGHT, SUPPORT_AREA)

    workpiece_model.report_rectangle_piece((42, 177), (936, 600))

    workpiece_model.report_round_peace((206, 394), 139)
    workpiece_model.report_round_peace((500, 394), 104)
    workpiece_model.report_round_peace((700, 438), 17)
    workpiece_model.report_round_peace((700, 366), 17)
    workpiece_model.report_round_peace((700, 288), 19)

    return workpiece_model.compute_heat_map()

def compute_bars_location(workpiece_heat_map):
    bar_model = BarModel(workpiece_heat_map, WORKPIECE_WIDTH, AVAILABLE_BARS, BAR_SIZE, SECURITY_DISTANCE_BARS)
    bars_location = bar_model.compute_bar_location()
    return bar_model, bars_location

import sys
def compute_suction_cup_location(workpiece_heat_map, bar_used, bars_location):
    suction_cups_image = np.zeros(np.array(workpiece_heat_map).shape)
    suction_cups_locators = []
    results = []
    columns = []

    i = 0
    n_threads = bar_used
    with ThreadPoolExecutor(n_threads) as executor:
        for column in bars_location:
            np.set_printoptions(threshold=sys.maxsize)

            heat_map_bar = workpiece_heat_map[:, column: column + BAR_SIZE]
            suction_cups_locators.append(SuctionCupModel(heat_map_bar, WORKPIECE_HEIGHT, AVAILABLE_SUCTIONS_CUPS, BAR_SIZE,
                                                  SUCTION_CUPS_SIZE, SECURITY_DISTANCE_SUCTION_CUPS))
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

    bar_used = bar_model.get_num_bars_used()
    bars_image = bar_model.get_bar_position_image()

    suction_cups_locators, suction_cups_image = compute_suction_cup_location(workpiece_heat_map, bar_used,
                                                                             bars_location)

    fig, axs = plt.subplots(1, 3, figsize=(10, 10))
    axs[0].imshow(np.flipud(workpiece_processing))
    axs[1].imshow(np.flipud(workpiece_heat_map))
    axs[2].imshow(np.flipud(workpiece_processing + bars_image + suction_cups_image))

    plt.show()
