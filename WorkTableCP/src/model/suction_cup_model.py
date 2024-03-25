import numpy as np
import sys
from utility.locator_service import LocatorService

class SuctionCupModel():

    def __init__(self, heat_map_bar, workpiece_height, available_suction_cups, cup_width, cup_height, security_distance):
        self.heat_map_bar = heat_map_bar
        self.workpiece_height = workpiece_height
        self.available_suction_cups = available_suction_cups
        self.cup_width = cup_width
        self.cup_height = cup_height
        self.security_distance = security_distance
        self.max_suction_cups_in_bar = round(workpiece_height / cup_height)
        self.max_suction_cups_positions = workpiece_height - cup_height + 1
        self.suction_cups_location = None

    def __compute_suction_cups_profit(self):
        profit = np.zeros(self.max_suction_cups_positions, dtype=int)
        for c in range(len(profit)):
            flag_pass_trough_process = False
            for i in range(c, c + self.cup_height):
                for j in range(0, self.cup_width):
                    if self.heat_map_bar[i][j] == - 1:
                        flag_pass_trough_process = True
                        profit[c] = 0
                        break
                    else:
                        profit[c] += self.heat_map_bar[i][j]
                if flag_pass_trough_process:
                    break

        return profit.tolist()

    def __compute_suction_cups_space_occupied(self):
        return [self.cup_height + self.security_distance] * (self.max_suction_cups_in_bar - 1) + [self.cup_height]

    def compute_suction_cups_location(self):
        profit_for_suction_cup = self.__compute_suction_cups_profit()
        suction_cup_space_occupied = self.__compute_suction_cups_space_occupied()

        suction_cup_positioning_model = LocatorService(self.workpiece_height, self.max_suction_cups_in_bar,
                                                       self.max_suction_cups_positions,
                                                       suction_cup_space_occupied, profit_for_suction_cup)

        self.suction_cups_location = suction_cup_positioning_model.resolve_instance()
        return self.suction_cups_location

    def get_suction_cup_position_image(self, workpiece_shape, column_index):
        cup_position_image = np.zeros(workpiece_shape, dtype=int)
        for value in self.suction_cups_location:
            cup_position_image[value:value + self.cup_height, column_index:column_index + self.cup_width] = 1
        return cup_position_image