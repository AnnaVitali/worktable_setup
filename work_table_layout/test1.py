import numpy as np
from itertools import product
from locator_service import LocatorService
from keypoint_detector_service import KeypointDetectorService

FLAG_DEBUG = False
SOLVER = 'gecode'

workpiece_processing = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

workpiece_width = np.array(workpiece_processing).shape[1]
workpiece_height = np.array(workpiece_processing).shape[0]

available_bars = 12
bar_width = 2
horizontal_security_distance = 1

cup_height = 2
available_suction_cups = 24
vertical_security_distance = 2

heat_map_model = KeypointDetectorService(workpiece_processing, workpiece_width, workpiece_height)

heat_map_model.instantiate_model(SOLVER)

result = heat_map_model.resolve_instance()

workpiece_heat_map = result["workpiece_heat_map"]

max_bars_position = workpiece_width - bar_width + 1
score_for_columns = [sum(idx) for idx in zip(*workpiece_heat_map)]
profit_for_bar = [sum(score_for_columns[i:i + bar_width]) for i in range(max_bars_position)]
bar_space_occupied = [bar_width + horizontal_security_distance] * (max_bars_position - 1) + [bar_width]

bar_positioning_model = LocatorService(workpiece_width, available_bars, horizontal_security_distance,
                                         max_bars_position, bar_space_occupied, profit_for_bar)
bar_positioning_model.instantiate_model(SOLVER)

result_bar_positioning = bar_positioning_model.resolve_instance()

where_bar_are_positioned = result_bar_positioning["object_selected"]
bar_column_index = np.where(where_bar_are_positioned)[0]

bars_position_truth_map = np.zeros(np.array(workpiece_processing).shape, dtype=int)

for j in range(max_bars_position):
    if where_bar_are_positioned[j]:
        bars_position_truth_map[:, j:j + bar_width] = 1

num_bars_used = sum(where_bar_are_positioned)

max_suction_cups_for_bar = workpiece_height - cup_height + 1
max_suction_cups_for_workpiece = max_suction_cups_for_bar * sum(where_bar_are_positioned)
suction_cups_space_occupied = [cup_height + vertical_security_distance] * (max_suction_cups_for_bar - 1) + [cup_height]

profit_for_suction_cup = np.zeros((max_suction_cups_for_bar, num_bars_used), dtype=int)

for bar_index, column_index in enumerate(bar_column_index[:num_bars_used]):
    for suction_cup_index, i_offset, j_offset in product(range(max_suction_cups_for_bar), range(cup_height),
                                                         range(bar_width)):
        i = suction_cup_index + i_offset
        j = column_index + j_offset
        if i < len(workpiece_heat_map) and j < len(workpiece_heat_map[0]):
            if workpiece_heat_map[i][j] == -1:
                profit_for_suction_cup[suction_cup_index][bar_index] = 0
                break
            else:
                profit_for_suction_cup[suction_cup_index][bar_index] += workpiece_heat_map[i][j]

where_suction_cups_are_positioned = np.zeros(profit_for_suction_cup.shape, dtype=int)

for i in range(0, num_bars_used):
    suction_cup_profit = profit_for_suction_cup[:, i]

    suction_cup_positioning_model = LocatorService(workpiece_height, available_suction_cups,
                                                     vertical_security_distance,
                                                     max_suction_cups_for_bar, suction_cups_space_occupied,
                                                     suction_cup_profit)
    suction_cup_positioning_model.instantiate_model(SOLVER)

    result_suction_cups_positioning_in_bar = suction_cup_positioning_model.resolve_instance()
    where_suction_cups_are_positioned[:, i] = result_suction_cups_positioning_in_bar["object_selected"]

suction_cups_position_truth_map = np.zeros(np.array(workpiece_processing).shape, dtype=int)

for i in range(max_suction_cups_for_bar):
    for bar_index, column_index in enumerate(bar_column_index[:num_bars_used]):
        if where_suction_cups_are_positioned[i][bar_index]:
            suction_cups_position_truth_map[i:i+cup_height, column_index:column_index + bar_width] = 1

# for bar_index, column_index in enumerate(bar_column_index[:bar_used]):
#     print(f"({column_index})")
#     for suction_cup_index in range(max_suction_cups_for_bar):
#         for i in range(suction_cup_index, suction_cup_index + cup_height):
#             for j in range(column_index, column_index + bar_width):
#                 print(f"({i}, {j})")
#                 profit_for_suction_cup[suction_cup_index][bar_index] += workpiece_heat_map[i][j]


# for column in range(0, bar_used):
#     column_index = bar_column_index[column]
#     for c in range(0, max_suction_cups_for_bar):
#         print(f"({column_index})")
#         for i in range(c, c + cup_height):
#             for j in range(column_index, column_index + bar_width):
#                 print(f"({i}, {j})")
#                 profit_for_suction_cup[c][column] += workpiece_heat_map[i][j]
#
# for bar in range(bar_used):
# column_index = bar_column_index[bar]
# for cup_row_index in range(max_suction_cups_for_bar):
#     profit_for_suction_cup[cup_row_index][bar] = np.sum(
#         workpiece_heat_map[cup_row_index: cup_row_index + cup_height][
#         column_index:column_index + bar_width])

final_result = suction_cups_position_truth_map + bars_position_truth_map

utility.debug(True, f"workpiece heat map \n {np.array(workpiece_heat_map)}")
utility.debug(FLAG_DEBUG, f"score for column {score_for_columns}")
utility.debug(FLAG_DEBUG, f"profit for bars{profit_for_bar}")
utility.debug(FLAG_DEBUG, f"space occupied by bars {bar_space_occupied}")
utility.debug(FLAG_DEBUG, f"bar selected {where_bar_are_positioned}")
utility.debug(True, f"Bar position truth map \n {bars_position_truth_map}")
utility.debug(FLAG_DEBUG, f"profit for suction cup \n {profit_for_suction_cup}")
utility.debug(FLAG_DEBUG, f"where suction cups are positioned in bars \n {where_suction_cups_are_positioned}")
utility.debug(True, f"suction cups position truth map \n {suction_cups_position_truth_map}")
utility.debug(True, f"final result\n {final_result}")
