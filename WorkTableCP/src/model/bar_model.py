import numpy as np
import sys
from utility.locator_service import LocatorService

class BarModel():

    def __init__(self, workpiece_heat_map, workpiece_width, available_bars, bar_width, security_distance):
        self.workpiece_width = workpiece_width
        self.available_bars = available_bars
        self.bar_width = bar_width
        self.security_distance = security_distance
        self.max_bar_positions = workpiece_width - bar_width + 1
        self.workpiece_heat_map = workpiece_heat_map
        self.bar_location = None

    def __compute_bars_location_profit(self, workpiece_heat_map):
        score_for_columns = [sum(idx) for idx in zip(*workpiece_heat_map)]
        return [int(sum(score_for_columns[i:i + self.bar_width])) for i in range(self.max_bar_positions)]

    def __compute_bars_space_occupied(self):
        return [self.bar_width + self.security_distance] * (self.available_bars - 1) + [self.bar_width]

    def compute_bar_location(self):
        np.set_printoptions(threshold=sys.maxsize)
        profit_for_bar = self.__compute_bars_location_profit(self.workpiece_heat_map)
        print(f"profit 772: {profit_for_bar[772]}")
        print(f"profit 773: {profit_for_bar[773]}")
        bar_space_occupied = self.__compute_bars_space_occupied()

        bar_positioning_model = LocatorService(self.workpiece_width, self.available_bars,
                                                 self.max_bar_positions, bar_space_occupied, profit_for_bar)

        self.bar_location = bar_positioning_model.resolve_instance()
        return self.bar_location

    def get_bar_position_image(self):
        bars_position_image = np.zeros(self.workpiece_heat_map.shape, dtype=int)

        for value in self.bar_location:
            bars_position_image[:, value:value + self.bar_width] = 1
        return bars_position_image

    def get_num_bars_used(self):
        return sum(self.bar_location)
