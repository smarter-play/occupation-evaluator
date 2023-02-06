from math import *
from datetime import datetime


def noise(n: float):
    return abs(modf(sin(n) * 43758.5453123)[0])


def is_unplayable_day(date: datetime):
    return noise(date.year * 365 + date.month * 31 + date.day) <= \
        [0.9, 0.8, 0.6, 0.38, 0.3, 0.1, 0.08, 0.07, 0.1, 0.3, 0.79, 0.9][date.month - 1]

