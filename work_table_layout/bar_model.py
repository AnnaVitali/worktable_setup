import numpy as np
from locator_service import LocatorService

class BarModel():

    def __init__(self, workpiece_width, available_bars, bar_width, security_distance):
        self.workpiece_width = workpiece_width
        self.available_bars = available_bars
        self.bar_width = bar_width
        self.security_distance = security_distance
        self.max_bar_positions = workpiece_width - bar_width + 1
        self.bar_location = None

    def __compute_bars_location_profit(self, workpiece_heat_map):
        score_for_columns = [sum(idx) for idx in zip(*workpiece_heat_map)]
        return [sum(score_for_columns[i:i + self.bar_width]) for i in range(self.max_bar_positions)]

    def __compute_bars_space_occupied(self):
        return [self.bar_width + self.security_distance] * (self.max_bar_positions - 1) + [self.bar_width]

    def compute_bar_location(self, workpiece_heat_map, solver_name):

        profit_for_bar = self.__compute_bars_location_profit(workpiece_heat_map)
        bar_space_occupied = self.__compute_bars_space_occupied()

        bar_positioning_model = LocatorService(self.workpiece_width, self.available_bars, self.security_distance,
                                                 self.max_bar_positions, bar_space_occupied, profit_for_bar)
        bar_positioning_model.instantiate_model(solver_name)

        self.bar_location = bar_positioning_model.resolve_instance()["object_selected"]
        return self.bar_location

    def get_bar_position_image(self, workpiece_shape):
        bars_position_image = np.zeros(workpiece_shape, dtype=int)

        for j in range(self.max_bar_positions):
            if self.bar_location[j]:
                bars_position_image[:, j:j + self.bar_width] = 1
        return bars_position_image

    def get_num_bars_used(self):
        return sum(self.bar_location)

