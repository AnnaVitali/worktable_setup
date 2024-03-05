import numpy as np
from skimage import draw
import matplotlib.pyplot as plt
from workpiece_model import WorkpieceModel
from bar_model import BarModel
from suction_cup_model import SuctionCupModel

FLAG_DEBUG = False
SOLVER = 'highs'

workpiece_processing = np.zeros((800, 1000), dtype=int)
rr, cc = draw.rectangle_perimeter((177, 42), extent=(422, 893), shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1


rr, cc = draw.circle_perimeter(394, 206, radius=139, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1

rr, cc = draw.circle_perimeter(394, 206, radius=123, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1

rr, cc = draw.circle_perimeter(393, 499, radius=104, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1

rr, cc = draw.circle_perimeter(393, 499, radius=86, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1

rr, cc = draw.circle_perimeter(438, 700, radius=17, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1


rr, cc = draw.circle_perimeter(366, 701, radius=17, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1


rr, cc = draw.circle_perimeter(288, 703, radius=18, shape=workpiece_processing.shape)
workpiece_processing[rr,cc] = -1

workpiece_width = np.array(workpiece_processing).shape[1]
workpiece_height = np.array(workpiece_processing).shape[0]

available_bars = 8
bar_width = 145
horizontal_security_distance = 100

available_suction_cups = 24
cup_height = 145
vertical_security_distance = 145

workpiece = WorkpieceModel(workpiece_processing, workpiece_width, workpiece_height)
workpiece_heat_map = workpiece.compute_heat_map(SOLVER)

bar_locator = BarModel(workpiece_width, available_bars, bar_width, horizontal_security_distance)
bar_location = bar_locator.compute_bar_location(workpiece_heat_map, SOLVER)

bar_location_image = bar_locator.get_bar_position_image(np.array(workpiece_processing).shape)
bar_used = bar_locator.get_num_bars_used()

suction_cups_locator = [SuctionCupModel(workpiece_height, available_suction_cups, bar_width, cup_height,
                                          vertical_security_distance) for i in range(0, bar_used)]
suction_cups_location = np.zeros(bar_used, dtype=int)
suction_cups_image = np.zeros(np.array(workpiece_processing).shape)

i = 0
for column, bar_present in enumerate(bar_location):
    if bar_present:
        heat_map_bar = np.array(workpiece_heat_map)[:, column: column + bar_width]
        suction_cups_locator[i].compute_suction_cups_location(heat_map_bar, SOLVER)
        suction_cups_image += suction_cups_locator[i].get_suction_cup_position_image(np.array(workpiece_processing).shape, column)
        i += 1

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(8,8))
ax1.imshow(workpiece_processing)
ax2.imshow(workpiece_heat_map)
ax3.imshow(bar_location_image + suction_cups_image + workpiece_processing)

plt.show()