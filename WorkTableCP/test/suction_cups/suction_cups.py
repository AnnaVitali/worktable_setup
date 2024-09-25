import sys
import os

import matplotlib.pyplot as plt
import numpy as np

sys.path.append(os.path.abspath('../..'))
sys.path.append(os.path.abspath('../../src'))

from src.suction_cups.suction_cup import SuctionCup

if __name__ == '__main__':
    suction_cup_name = 'suction_cup'
    suction_cup_height = 65
    suction_cup_width = 180

    # Instantiate and test suction cup with rotation
    suction_cup = SuctionCup(suction_cup_name, suction_cup_width, suction_cup_height)
    matrix_representation = suction_cup.get_matrix_representation_with_support()

    matrix_representation = suction_cup.rotate(45)

    # Visualize the result
    plt.imshow(matrix_representation, cmap='gray', aspect='auto', interpolation='nearest')
    plt.title("Suction Cup")
    plt.show()