import numpy as np
from locator_service import LocatorService

class SuctionCupModel():

    def __init__(self, workpiece_height, available_suction_cups, cup_width, cup_height, security_distance):
        self.workpiece_height = workpiece_height
        self.available_suction_cups = available_suction_cups
        self.cup_width = cup_width
        self.cup_height = cup_height
        self.security_distance = security_distance
        self.max_suction_cups_per_bar = workpiece_height - cup_height + 1
        self.suction_cups_location = None

    def __compute_suction_cups_profit(self, heat_map_bar):
        height, width = heat_map_bar.shape
        profit = np.zeros(self.max_suction_cups_per_bar, dtype=int)
        for c in range(len(profit)):
            flag_pass_trough_process = False
            for i in range(c, c + self.cup_height):
                for j in range(0, width):
                    if flag_pass_trough_process: break
                    if heat_map_bar[i][j] == - 1:
                        flag_pass_trough_process = True
                        profit[c] = 0
                        break
                    else:
                        profit[c] += heat_map_bar[i][j]
        return profit

    def __compute_suction_cups_space_occupied(self):
        return [self.cup_height + self.security_distance] * (self.max_suction_cups_per_bar - 1) + [self.cup_height]

    def compute_suction_cups_location(self, heat_map_bar, solver_name):
        profit_for_suction_cup = self.__compute_suction_cups_profit(heat_map_bar)
        suction_cup_space_occupied = self.__compute_suction_cups_space_occupied()

        suction_cup_positioning_model = LocatorService(self.workpiece_height, self.available_suction_cups,
                                                         self.security_distance, self.max_suction_cups_per_bar,
                                                         suction_cup_space_occupied, profit_for_suction_cup)
        suction_cup_positioning_model.instantiate_model(solver_name)

        self.suction_cups_location = suction_cup_positioning_model.resolve_instance()["object_selected"]
        return self.suction_cups_location

    def get_suction_cup_position_image(self, workpiece_shape, column_index):
        cup_position_image = np.zeros(workpiece_shape, dtype=int)

        for i in range(self.max_suction_cups_per_bar):
            if self.suction_cups_location[i]:
                cup_position_image[i:i + self.cup_height, column_index:column_index + self.cup_width] = 1
        return cup_position_image