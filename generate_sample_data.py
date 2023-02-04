from datetime import datetime, timedelta
from math import *
import numpy as np
import numpy.typing
import matplotlib.pyplot as plt


NUM_DAY_SAMPLES = 24 * 60
DAY_SAMPLES = np.linspace(0, 23.99, NUM_DAY_SAMPLES)


def gaussian(x, mu, var):
    return (1 / sqrt(2 * pi * var)) * exp(-((x - mu) ** 2 / (2 * var)))


def noise(n: float):
    return abs(modf(sin(n) * 43758.5453123)[0])


# ------------------------------------------------------------------------------------------------
# DayType
# ------------------------------------------------------------------------------------------------


class DayType:
    name: str
    
    accelerometer_data_distribution: numpy.typing.ArrayLike
    basket_distribution: numpy.typing.ArrayLike
    people_detected_distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int
    num_basket_samples: int
    num_people_detected_samples: int

    def __init__(self):
        pass

    def draw_accelerometer_data_samples(self):
        n = round(self.num_accelerometer_data_samples + self.num_accelerometer_data_samples * np.random.normal(scale=0.2))
        accelerometer_data_samples = np.random.choice(DAY_SAMPLES, n, p=self.accelerometer_data_distribution)
        return accelerometer_data_samples

    def draw_basket_samples(self):
        n = round(self.num_basket_samples + self.num_basket_samples * np.random.normal(scale=0.2))
        basket_samples = np.random.choice(DAY_SAMPLES, n, p=self.basket_distribution)
        return basket_samples

    def draw_people_detected_samples(self):
        n = round(self.num_people_detected_samples + self.num_people_detected_samples * np.random.normal(scale=0.2))
        people_detected_samples = np.random.choice(DAY_SAMPLES, n, p=self.people_detected_distribution)
        return people_detected_samples


# ------------------------------------------------------------------------------------------------
# UnplayableDay
# ------------------------------------------------------------------------------------------------


class UnplayableDay(DayType):
    name: str = 'Unplayable Day'

    accelerometer_data_distribution: numpy.typing.ArrayLike
    basket_distribution: numpy.typing.ArrayLike
    people_detected_distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int = 20
    num_basket_samples: int = 3
    num_people_detected_samples: int = 50

    def __init__(self):
        self.accelerometer_data_distribution = self.generate_accelerometer_data_distribution()
        self.basket_distribution = self.generate_basket_distribution()
        self.people_detected_distribution = self.generate_people_detected_distribution()

    @staticmethod
    def generate_accelerometer_data_distribution():
        mu = (14.5 + 17) / 2
        var = 1000

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    @staticmethod
    def generate_basket_distribution():
        mu = (14.5 + 17) / 2
        var = 1

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    @staticmethod
    def generate_people_detected_distribution():
        mu = (8 + 21) / 2
        var = 10

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    def is_(date: datetime):
        return noise(date.month * 31 + date.day) <= [0.9, 0.8, 0.6, 0.38, 0.3, 0.1, 0.08, 0.07, 0.1, 0.3, 0.79, 0.9][date.month - 1]


# ------------------------------------------------------------------------------------------------
# BusyDay
# ------------------------------------------------------------------------------------------------


class BusyDay(DayType):
    name: str = "Busy Day"

    accelerometer_data_distribution: numpy.typing.ArrayLike
    basket_distribution: numpy.typing.ArrayLike
    people_detected_distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int = 40
    num_basket_samples: int = 20
    num_people_detected_samples: int = 50

    def __init__(self):
        self.accelerometer_data_distribution = self.generate_accelerometer_data_distribution()
        self.basket_distribution = self.generate_basket_distribution()
        self.people_detected_distribution = self.generate_people_detected_distribution()
    
    @staticmethod
    def generate_accelerometer_data_distribution():
        mu = (17.5 + 19.5) / 2
        var = 29

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    @staticmethod
    def generate_basket_distribution():
        mu = (17.5 + 19.5) / 2
        var = 1

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    @staticmethod
    def generate_people_detected_distribution():
        mu = (8 + 21) / 2
        var = 20

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    @staticmethod
    def is_(date: datetime):
        busy = True
        busy &= (1 <= date.month <= 5) or (9 <= date.month <= 12) # January to May OR September to December
        busy &= not date.weekday() == 6 # Sunday
        busy &= not (date.month == 12 and 23 <= date.day <= 31) # Christmas holiday
        busy &= not (date.month == 1 and 1 <= date.day <= 6)
        return busy


# ------------------------------------------------------------------------------------------------
# PlayableDay
# ------------------------------------------------------------------------------------------------


class PlayableDay(DayType):
    name: str = 'Playable Day'

    accelerometer_data_distribution: numpy.typing.ArrayLike
    basket_distribution: numpy.typing.ArrayLike
    people_detected_distribution: numpy.typing.ArrayLike

    num_accelerometer_data_samples: int = 100
    num_basket_samples: int = 50
    num_people_detected_samples: int = 100

    def __init__(self):
        self.accelerometer_data_distribution = self.generate_accelerometer_data_distribution()
        self.basket_distribution = self.generate_basket_distribution()
        self.people_detected_distribution = self.generate_people_detected_distribution()

    @staticmethod
    def generate_accelerometer_data_distribution():
        mu1 = (9 + 11) / 2
        var1 = 100
        peak1 = 1

        mu2 = (15 + 17) / 2
        var2 = 100
        peak2 = 3

        distr = np.vectorize(lambda x: peak1 * gaussian(x, mu1, var1))(DAY_SAMPLES) + \
            np.vectorize(lambda x: peak2 * gaussian(x, mu2, var2))(DAY_SAMPLES)

        distr /= np.sum(distr)

        return distr
    
    @staticmethod
    def generate_basket_distribution():
        mu1 = (9 + 11) / 2
        var1 = 1
        peak1 = 1

        mu2 = (15 + 17) / 2
        var2 = 1
        peak2 = 3

        distr = np.vectorize(lambda x: peak1 * gaussian(x, mu1, var1))(DAY_SAMPLES) + \
            np.vectorize(lambda x: peak2 * gaussian(x, mu2, var2))(DAY_SAMPLES)

        distr /= np.sum(distr)

        return distr
    
    @staticmethod
    def generate_people_detected_distribution():
        mu1 = (9 + 11) / 2
        var1 = 2
        peak1 = 1

        mu2 = (15 + 17) / 2
        var2 = 6
        peak2 = 5

        distr = np.vectorize(lambda x: peak1 * gaussian(x, mu1, var1))(DAY_SAMPLES) + \
            np.vectorize(lambda x: peak2 * gaussian(x, mu2, var2))(DAY_SAMPLES)

        distr /= np.sum(distr)

        return distr
    
    @staticmethod
    def is_(date: datetime):
        return not BusyDay.is_(date) and UnplayableDay.is_(date)


# ------------------------------------------------------------------------------------------------


unplayable_day = UnplayableDay()
busy_day = BusyDay()
playable_day = PlayableDay()


def sample_measurements_for_day(date: datetime, verbose=True):
    day_type = None

    if UnplayableDay.is_(date):
        day_type = unplayable_day
    elif BusyDay.is_(date):
        day_type = busy_day
    else: # PlayableDay
        day_type = playable_day

    print(f"{date.strftime('%d %B %Y')} ({date.strftime('%A')}) → {day_type.name}")

    accelerator_data_samples = day_type.draw_accelerometer_data_samples()
    basket_samples = day_type.draw_basket_samples()
    people_detected_samples = day_type.draw_people_detected_samples()

    if verbose:
        fig, ax = plt.subplots(nrows=3)

        fig.suptitle(f"{date.strftime('%d %B %Y')} ({date.strftime('%A')}) → {day_type.name}")

        ax[0].bar(basket_samples, np.full(len(basket_samples), 1), color='r', width=0.1)
        ax[0].set_xlim([0, 24])
        ax[0].set_ylim([0, 2])
        ax[0].set_xticks(range(24))
        ax[0].set_title("Baskets")
        
        ax[1].bar(accelerator_data_samples, np.full(len(accelerator_data_samples), 1), color='b', width=0.1)
        ax[1].set_xlim([0, 24])
        ax[1].set_ylim([0, 2])
        ax[1].set_xticks(range(24))
        ax[1].set_title("Accelerometer data")

        ax[2].bar(people_detected_samples, np.full(len(people_detected_samples), 1), color='g', width=0.1)
        ax[2].set_xlim([0, 24])
        ax[2].set_ylim([0, 2])
        ax[2].set_xticks(range(24))
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


def show_day_type_distributions(day_type: DayType, **kwargs):
    fig, ax = plt.subplots(nrows=3)
    
    fig.suptitle(day_type.name)

    ax[0].plot(DAY_SAMPLES, day_type.accelerometer_data_distribution, **kwargs)
    ax[0].set_xlim([0, 24])
    ax[0].set_title("Accelerometer data distribution")
    ax[0].set_xticks(range(24))

    ax[1].plot(DAY_SAMPLES, day_type.basket_distribution, **kwargs)
    ax[1].set_xlim([0, 24])
    ax[1].set_title("Basket distribution")
    ax[1].set_xticks(range(24))

    ax[2].plot(DAY_SAMPLES, day_type.people_detected_distribution, **kwargs)
    ax[2].set_xlim([0, 24])
    ax[2].set_title("People detected distribution")
    ax[2].set_xticks(range(24))

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    verbose=True

    try:
        if verbose:
            show_day_type_distributions(unplayable_day)
            show_day_type_distributions(busy_day)
            show_day_type_distributions(playable_day)

        sample_measurements_between(datetime(2016, 1, 1), datetime(2016, 12, 31), verbose=verbose)
    except KeyboardInterrupt as _:
        pass

