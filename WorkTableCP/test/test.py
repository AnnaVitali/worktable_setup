import sys
import os

sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
from src.utility.workpiece_drawer import WorkpieceDrawer
from src.model.workpiece_heat_map_model import WorkpieceHeatMapModel
from src.model.bar_model import BarModel
from src.model.suction_cup_model import SuctionCupModel
from src.parameter.machine import Machine
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import wait
from sympy import Point2D
from matplotlib.colors import ListedColormap

WORKPIECE_WIDTH = 715
WORKPIECE_HEIGHT = 400
SECURITY_DISTANCE_SUCTION_CUPS = 100
SECURITY_DISTANCE_BARS = 120


def get_workpiece_processing():
    workpiece_draw = WorkpieceDrawer(WORKPIECE_WIDTH, WORKPIECE_HEIGHT)

    workpiece_draw.draw_perimeter_piece()

    contouring_thickness = 20
    workpiece_draw.draw_thick_line((665, 394), (20, 262), contouring_thickness, "up")
    workpiece_draw.draw_thick_line((20, 262), (20, 135), contouring_thickness, "left")
    workpiece_draw.draw_thick_line((20, 135), (665, 4), contouring_thickness, "down")
    workpiece_draw.draw_thick_line((665, 4), (689, 17), contouring_thickness, "right")
    workpiece_draw.draw_thick_line((689, 17), (689, 380), contouring_thickness, "right")
    workpiece_draw.draw_thick_line((689, 380), (665, 394), contouring_thickness, "right")

    workpiece_draw.draw_circle_line((65, 198), 31, 20)

    thickness_small_circles = 10
    workpiece_draw.draw_circle_line((654, 354), 10, thickness_small_circles)
    workpiece_draw.draw_circle_line((675, 198), 10, thickness_small_circles)
    workpiece_draw.draw_circle_line((654, 43), 10, thickness_small_circles)

    return workpiece_draw.get_workpiece_processing_draw()


if __name__ == '__main__':
    # Define the sides of the polygon and its vertices
    sides = [((665, 394), (20, 262)), ((20, 262), (20, 135)), ((20, 135), (665, 4)), ((665, 4), (689, 17)),
             ((689, 17), (689, 380)), ((689, 380), (665, 394))]
    points = [(665, 394), (20, 262), (20, 135), (665, 4), (689, 17), (689, 380), (665, 394)]

    # Plot the polygon
    x, y = zip(*points)  # Extract x and y coordinates
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, '-o', label="Polygon")  # Draw the polygon and mark vertices
    plt.scatter(*zip(*points), color='red', zorder=5, label="Vertices")  # Highlight vertices

    # Add labels for vertices
    for idx, (px, py) in enumerate(points[:-1]):  # Exclude the last repeated vertex
        plt.text(px + 5, py + 5, f"P{idx+1}", color="blue", fontsize=10)

    # Add labels and grid for better readability
    plt.title("Polygon with Highlighted Vertices")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.show()
