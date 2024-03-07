import numpy as np
import sys
from skimage import draw
import matplotlib.pyplot as plt
from workpiece_model import WorkpieceModel
from bar_model import BarModel
from suction_cup_model import SuctionCupModel

SOLVER = 'highs'

workpiece_processing = np.zeros((398, 715), dtype=int)

#1
rr, cc, _ = draw.line_aa(59, 406, 3, 665)
workpiece_processing[rr, cc] = -1

#2
rr, cc, _ = draw.line_aa(3, 665, 17, 700)
workpiece_processing[rr, cc] = -1

#3
rr, cc, _ = draw.line_aa(17, 700, 379, 700)
workpiece_processing[rr, cc] = -1

#4
rr, cc, _ = draw.line_aa(379, 700, 393, 665)
workpiece_processing[rr, cc] = -1

#5
rr, cc, _ = draw.line_aa(393, 665, 262, 10)
workpiece_processing[rr, cc] = -1

#6
rr, cc, _= draw.line_aa(262, 10, 135, 10)
workpiece_processing[rr, cc] = -1

#7
rr, cc, _= draw.line_aa(135, 10, 59, 406)
workpiece_processing[rr, cc] = -1


for i in range(0, 20):
    rr, cc = draw.circle_perimeter(198, 65, radius=31 + i, shape=workpiece_processing.shape)
    workpiece_processing[rr, cc] = -1

for i in range(0, 10):
    rr, cc = draw.circle_perimeter(354, 654, radius=10 + i, shape=workpiece_processing.shape)
    workpiece_processing[rr, cc] = -1

    rr, cc = draw.circle_perimeter(198, 675, radius=10 + i, shape=workpiece_processing.shape)
    workpiece_processing[rr, cc] = -1

    rr, cc = draw.circle_perimeter(43, 654, radius=10 + i, shape=workpiece_processing.shape)
    workpiece_processing[rr, cc] = -1

rr, cc = draw.polygon([3, 17, 379, 393, 262, 135, 59], [665, 700, 700, 665, 10, 10, 406], shape=workpiece_processing.shape)
workpiece_processing[rr, cc] = np.where(workpiece_processing[rr, cc] != -1,  workpiece_processing[rr, cc]+2,
                                        workpiece_processing[rr, cc])

rr, cc = draw.disk((198, 65), radius=30, shape=workpiece_processing.shape)
workpiece_processing[rr, cc] = np.where(workpiece_processing[rr, cc] != -1,  workpiece_processing[rr, cc]+2,
                                        workpiece_processing[rr, cc])

rr, cc = draw.disk((354, 654), radius=10, shape=workpiece_processing.shape)
workpiece_processing[rr, cc] = np.where(workpiece_processing[rr, cc] != -1,  workpiece_processing[rr, cc]+2,
                                        workpiece_processing[rr, cc])

rr, cc = draw.disk((198, 675), radius=10, shape=workpiece_processing.shape)
workpiece_processing[rr, cc] = np.where(workpiece_processing[rr, cc] != -1,  workpiece_processing[rr, cc]+2,
                                        workpiece_processing[rr, cc])

rr, cc = draw.disk((43, 654), radius=10, shape=workpiece_processing.shape)
workpiece_processing[rr, cc] = np.where(workpiece_processing[rr, cc] != -1,  workpiece_processing[rr, cc]+2,
                                        workpiece_processing[rr, cc])

plt.imshow(workpiece_processing)
plt.show()

workpiece_width = np.array(workpiece_processing).shape[1]
workpiece_height = np.array(workpiece_processing).shape[0]

available_bars = 8
bar_width = 145
horizontal_security_distance = 70

available_suction_cups = 24
cup_height = 145
vertical_security_distance = 20

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
        suction_cups_image += suction_cups_locator[i].get_suction_cup_position_image(
            np.array(workpiece_processing).shape, column)
        i += 1

np.set_printoptions(threshold=sys.maxsize)

np.set_printoptions(threshold=sys.maxsize)

#print(f"bars: \n{bar_location_image + suction_cups_image}")
#print(f"cups: \n{suction_cups_image}")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 8))
ax1.imshow(workpiece_processing)
ax2.imshow(workpiece_heat_map)
ax3.imshow(bar_location_image + suction_cups_image + workpiece_processing)

plt.show()
