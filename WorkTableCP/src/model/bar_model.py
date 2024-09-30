import numpy as np
from model.locator import Locator
from parameter.workings import Workings


class BarModel:

    def __init__(self, workpiece_heat_map, workpiece_width, available_bars, bar_width, security_distance):
        self.workpiece_width = workpiece_width
        self.available_bars = available_bars
        self.bar_width = bar_width
        self.security_distance = security_distance
        self.max_bar_positions = workpiece_width - bar_width + 1
        self.workpiece_heat_map = workpiece_heat_map
        self.bar_location = None

    def __compute_bars_location_profit(self, workpiece_heat_map):
        """Compute the profit for each potential bar location."""
        # Sum the values in each column (score) and calculate penalties for pass-through points
        score_for_columns = np.sum(workpiece_heat_map, axis=0)
        penalty_for_columns = np.sum(workpiece_heat_map == Workings.PASS_THROUGH_WORKING_POINT.value, axis=0)

        # Compute the profit for each possible bar position
        profit_for_columns = [
            np.sum(score_for_columns[i:i + self.bar_width]) - np.sum(penalty_for_columns[i:i + self.bar_width])
            for i in range(self.max_bar_positions)
        ]

        return profit_for_columns

    def __compute_bars_space_occupied(self):
        """Compute the space occupied by the bars."""
        #result = np.full(self.available_bars - 1, self.bar_width + self.security_distance).tolist() + [self.bar_width]
        #result.insert(0,0)
        return np.full(self.available_bars - 1, self.bar_width + self.security_distance).tolist() + [self.bar_width]

    def compute_bar_location(self):
        """Compute the optimal bar locations."""
        profit_for_bar = self.__compute_bars_location_profit(self.workpiece_heat_map)
        bar_space_occupied = self.__compute_bars_space_occupied()

        bar_positioning_model = Locator(self.workpiece_width, self.available_bars,
                                        self.max_bar_positions, bar_space_occupied, profit_for_bar)

        self.bar_location = bar_positioning_model.resolve_instance()
        return self.bar_location

    def get_bar_position_image(self):
        """Create a matrix showing the bar positions."""
        bars_position_image = np.zeros(self.workpiece_heat_map.shape, dtype=int)

        # Mark positions where bars are located
        for value in self.bar_location:
            bars_position_image[:, value:value + self.bar_width] = 1
        return bars_position_image

    def get_num_bars_used(self):
        """Get the number of bars used."""
        return len(self.bar_location)
