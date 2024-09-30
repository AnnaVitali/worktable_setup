import numpy as np
from model.locator import Locator
from parameter.workings import Workings


class SuctionCupModel:

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
        """Efficiently compute the profit for placing suction cups along the bar using NumPy."""
        # Initialize the profit array
        profit = np.zeros(self.max_suction_cups_positions, dtype=int)

        # Extract the relevant section of the heatmap (we only care about the part covered by suction cups)
        for c in range(self.max_suction_cups_positions):
            # Subset the part of the heatmap the cup will cover
            heat_map_slice = self.heat_map_bar[c:c + self.cup_height, :self.cup_width]

            # Check if there are any PASS_THROUGH_WORKING_POINTs
            if np.any(heat_map_slice == Workings.PASS_THROUGH_WORKING_POINT.value):
                profit[c] = 0  # Set profit to zero if a pass-through point is found
            else:
                # Sum the profits of all valid points in the slice
                profit[c] = np.sum(heat_map_slice)

        return profit.tolist()

    def __compute_suction_cups_space_occupied(self):
        """Compute the space occupied by each suction cup."""
        #result = [self.cup_height + self.security_distance] * (self.max_suction_cups_in_bar - 1) + [self.cup_height]
        #result.insert(0, 0)
        return [self.cup_height + self.security_distance] * (self.max_suction_cups_in_bar - 1) + [self.cup_height]

    def compute_suction_cups_location(self):
        """Compute the optimal suction cup locations."""
        profit_for_suction_cup = self.__compute_suction_cups_profit()
        suction_cup_space_occupied = self.__compute_suction_cups_space_occupied()

        suction_cup_positioning_model = Locator(self.workpiece_height, self.max_suction_cups_in_bar,
                                                self.max_suction_cups_positions,
                                                suction_cup_space_occupied, profit_for_suction_cup)

        self.suction_cups_location = suction_cup_positioning_model.resolve_instance()
        return self.suction_cups_location

    def get_suction_cup_position_image(self, workpiece_shape, column_index):
        """Create an image (matrix) showing the suction cup positions."""
        cup_position_image = np.zeros(workpiece_shape, dtype=int)
        for value in self.suction_cups_location:
            cup_position_image[value:value + self.cup_height, column_index:column_index + self.cup_width] = 1
        return cup_position_image
