from datetime import datetime, timedelta
from math import *
import numpy as np
import numpy.typing
import matplotlib.pyplot as plt


def gaussian(x, mu, var):
    return (1 / sqrt(2 * pi * var)) * exp(-((x - mu) ** 2 / (2 * var)))


class DayType:
    name: str
    
    distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int
    num_basket_samples: int
    num_people_detected_samples: int


def day_samples(num_samples: int):
    return np.linspace(0, 23.99, num_samples)


# ------------------------------------------------------------------------------------------------
# UnplayableDay
# ------------------------------------------------------------------------------------------------


class UnplayableDay(DayType):    
    name: str = 'Unplayable Day'

    distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int = 20
    num_basket_samples: int = 5
    num_people_detected_samples: int = 50


    def __init__(self, num_samples: int):
        self.num_samples = num_samples
        self.distribution = UnplayableDay.generate_distribution(num_samples)


    @staticmethod
    def is_(date: datetime):
        rainy = np.random.rand(1)[0] <= \
            [0.1, 0.1, 0.08, 0.06, 0.03, 0.01, 0.01, 0.02, 0.1, 0.15, 0.1, 0.1][date.month - 1]
        too_cold = np.random.rand(1)[0] <= \
            [0.8, 0.5, 0.2, 0.01, 0.001, 0.0001, 0.0001, 0.0001, 0.001, 0.1, 0.4, 0.7][date.month - 1]
        return rainy or too_cold


    @staticmethod
    def generate_distribution(num_samples: int):
        mu = (14.5 + 17) / 2
        var = 60

        x_arr = day_samples(num_samples)
        distr = np.vectorize(lambda x: gaussian(x, mu, var))(x_arr)
        
        distr /= np.sum(distr)

        return distr


# ------------------------------------------------------------------------------------------------
# BusyDay
# ------------------------------------------------------------------------------------------------


class BusyDay(DayType):
    name: str = "Busy Day"

    distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int = 40
    num_basket_samples: int = 20
    num_people_detected_samples: int = 50


    def __init__(self, num_samples: int):
        self.num_samples = num_samples
        self.distribution = BusyDay.generate_distribution(self.num_samples)


    @staticmethod
    def is_(date: datetime):
        busy = True
        busy &= (1 <= date.month <= 5) or (9 <= date.month <= 12) # January to May OR September to December
        busy &= not date.weekday() == 6 # Sunday
        busy &= not (date.month == 12 and 23 <= date.day <= 31) # Christmas holiday
        busy &= not (date.month == 1 and 1 <= date.day <= 6)
        return busy
    

    @staticmethod
    def generate_distribution(num_samples: int):
        mu = (17 + 19.5) / 2
        var = 1

        x_arr = day_samples(num_samples)
        distr = np.vectorize(lambda x: gaussian(x, mu, var))(x_arr)
        
        distr /= np.sum(distr)

        return distr


# ------------------------------------------------------------------------------------------------
# SunnyDay
# ------------------------------------------------------------------------------------------------


class SunnyDay(DayType):
    name: str = 'Sunny Day'

    distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int = 100
    num_basket_samples: int = 50
    num_people_detected_samples: int = 100


    def __init__(self, num_samples: int):
        self.num_samples = num_samples
        self.distribution = SunnyDay.generate_distribution(self.num_samples)


    @staticmethod
    def is_(date: datetime):
        return not BusyDay.is_(date) and UnplayableDay.is_(date)


    @staticmethod
    def generate_distribution(num_samples: int):
        mu1 = (9 + 11) / 2
        var1 = 1
        peak1 = 1

        mu2 = (15 + 17) / 2
        var2 = 1
        peak2 = 3

        x_arr = day_samples(num_samples)
        
        distr = \
            np.vectorize(lambda x: peak1 * gaussian(x, mu1, var1))(x_arr) + \
            np.vectorize(lambda x: peak2 * gaussian(x, mu2, var2))(x_arr)

        distr /= np.sum(distr)

        return distr


# ------------------------------------------------------------------------------------------------


NUM_SAMPLES = 24 * 60


sunny_day = SunnyDay(NUM_SAMPLES)
busy_day = BusyDay(NUM_SAMPLES)
unplayable_day = UnplayableDay(NUM_SAMPLES)


def sample_measurements_for_day(date: datetime, verbose=True):
    day_type = None

    if UnplayableDay.is_(date):
        day_type = unplayable_day
    elif BusyDay.is_(date):
        day_type = busy_day
    else: # SunnyDay
        day_type = sunny_day

    print(f"{date.strftime('%d %B %Y')} ({date.strftime('%A')}) → {day_type.name}")

    basket_samples = np.random.choice(day_samples(len(day_type.distribution)), day_type.num_basket_samples, p=day_type.distribution)
    accelerator_data_samples = np.random.choice(day_samples(len(day_type.distribution)), day_type.num_accelerometer_data_samples, p=day_type.distribution)
    people_detected_samples = np.random.choice(day_samples(len(day_type.distribution)), day_type.num_people_detected_samples, p=day_type.distribution)

    if verbose:
        fig, ax = plt.subplots(nrows=3)

        fig.suptitle(f"{date.strftime('%d %B %Y')} ({date.strftime('%A')}) → {day_type.name}")

        ax[0].bar(basket_samples, np.full(len(basket_samples), 1), color='r', width=0.1)
        ax[0].set_xlim([0, 24])
        ax[0].set_ylim([0, 2])
        ax[0].set_title("Baskets")
        
        ax[1].bar(accelerator_data_samples, np.full(len(accelerator_data_samples), 1), color='b', width=0.1)
        ax[1].set_xlim([0, 24])
        ax[1].set_ylim([0, 2])
        ax[1].set_title("Accelerometer data")

        ax[2].bar(people_detected_samples, np.full(len(people_detected_samples), 1), color='g', width=0.1)
        ax[2].set_xlim([0, 24])
        ax[2].set_ylim([0, 2])
        ax[2].set_title("People detected")

        fig.tight_layout()

        plt.show()


    return (
        basket_samples,
        accelerator_data_samples,
        people_detected_samples,
    )


def sample_measurements_between(from_date: datetime, to_date: datetime, verbose=True):
    date = from_date
    while (date <= to_date):
        sample_measurements_for_day(date, verbose)
        date += timedelta(days=1)


def show_day_type_distributions():
    fig, ax = plt.subplots(nrows=3)
    
    ax[0].plot(day_samples(NUM_SAMPLES), sunny_day.distribution)
    ax[0].set_xlim([0, 24])
    ax[0].set_title("Sunny day")

    ax[1].plot(day_samples(NUM_SAMPLES), busy_day.distribution)
    ax[1].set_xlim([0, 24])
    ax[1].set_title("Busy day")

    ax[2].plot(day_samples(NUM_SAMPLES), unplayable_day.distribution)
    ax[2].set_xlim([0, 24])
    ax[2].set_title("Unplayable day")

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    verbose=True

    try:
        if verbose:
            show_day_type_distributions()
        sample_measurements_between(datetime(2016, 1, 1), datetime(2016, 12, 31), verbose=verbose)
    except KeyboardInterrupt as _:
        pass

