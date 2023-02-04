from datetime import datetime
from enum import Enum
from math import *
from scipy.optimize import fsolve
import numpy as np


class DayType(Enum):
    SUNNY = 0,
    BUSY = 1,
    UNPLAYABLE = 2


def gaussian(x, mu, var):
    return (1 / sqrt(2 * pi * var)) * exp(-((x - mu) ** 2 / (2 * var)))


def find_gaussian_from_points(left_point, right_point, peak):
    x1, y1 = left_point
    x2, y2 = right_point

    def system(p):
        mu, var = p
        
        return (
            gaussian(x1, mu, var) - y1,
            gaussian(x2, mu, var) - y2,
        )

    mu, var = fsolve(system, (10, 1))

    return (mu, var)


def generate_sunny_day_distribution():
    #mu1, var1 = find_gaussian_from_points((9, 0.1), (11, 0.3), 1)
    mu2, var2 = find_gaussian_from_points((15, 0.2), (19, 0.2), 1)

    x_arr = np.linspace(0, 23.99, 4)
    
    distr = \
        np.vectorize(lambda x: gaussian(x, mu1, var1))(x_arr) + \
        np.vectorize(lambda x: gaussian(x, mu2, var2))(x_arr)

    distr /= np.amax(x_arr)

    return distr


def generate_busy_day_distribution():
    pass


def generate_unplayable_day_distribution():
    pass


def generate_sample_data(date: datetime):
    pass



if __name__ == "__main__":
    print("And it's with my immense pleasure to inform you that this is your Gaussian", generate_sunny_day_distribution())
