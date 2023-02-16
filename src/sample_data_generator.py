from datetime import datetime, timedelta
from math import *
import numpy as np
import numpy.typing
import matplotlib.pyplot as plt
from db import create_db_connection
from weather import is_unplayable_day


NUM_DAY_SAMPLES = 24 * 60
DAY_SAMPLES = np.linspace(0, 23.99, NUM_DAY_SAMPLES)

MOCK_BASKET_ID = 0x23232323


def gaussian(x, mu, var):
    return (1 / sqrt(2 * pi * var)) * exp(-((x - mu) ** 2 / (2 * var)))


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
    num_basket_samples: int = 4
    num_people_detected_samples: int = 50

    def __init__(self):
        self.accelerometer_data_distribution = self.generate_accelerometer_data_distribution()
        self.basket_distribution = self.generate_basket_distribution()
        self.people_detected_distribution = self.generate_people_detected_distribution()

    @staticmethod
    def generate_accelerometer_data_distribution():
        mu = (14.5 + 17) / 2
        var = 50

        distr = np.vectorize(lambda x: gaussian(x, mu, var))(DAY_SAMPLES)
        distr /= np.sum(distr)

        return distr

    @staticmethod
    def generate_basket_distribution():
        mu = (14.5 + 17) / 2
        var = 50

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
        return is_unplayable_day(date)


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

    num_accelerometer_data_samples: int = 150
    num_basket_samples: int = 50
    num_people_detected_samples: int = 200

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

    if verbose and date.month == 8:
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

    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()

    # Insert AccelerometerData
    db_cursor.executemany("""
        INSERT INTO accelerometer_data
            (basket_id,
                accel_x, accel_y, accel_z,
                gyro_x, gyro_y, gyro_z,
                temperature,
                timestamp)
        VALUES
            (%(basket_id)s, %(accel_x)s, %(accel_y)s, %(accel_z)s, %(gyro_x)s, %(gyro_y)s, %(gyro_z)s, %(temperature)s, %(timestamp)s)
    """, [
        { 'basket_id': MOCK_BASKET_ID,
            'accel_x': 23, 'accel_y': 23, 'accel_z': 23,
            'gyro_x': 23, 'gyro_y': 23, 'gyro_z': 23,
            'temperature': 23,
            'timestamp': date + timedelta(minutes=round(day_t * 60))
        } for day_t in accelerator_data_samples
    ])

    # Insert Basket
    db_cursor.executemany("""
        INSERT INTO score_data
            (basket_id, timestamp)
        VALUES
            (%(basket_id)s, %(timestamp)s)
    """, [
        { 'basket_id': MOCK_BASKET_ID,
            'timestamp': date + timedelta(minutes=round(day_t * 60))
        } for day_t in basket_samples
    ])

    # Insert PeopleDetected
    db_cursor.executemany("""
        INSERT INTO people_detected_data
            (basket_id, timestamp)
        VALUES
            (%(basket_id)s, %(timestamp)s)
    """, [
        { 'basket_id': MOCK_BASKET_ID,
            'timestamp': date + timedelta(minutes=round(day_t * 60))
        } for day_t in people_detected_samples
    ])

    db_cursor.close()
    db_connection.close()

    return (
        accelerator_data_samples,
        basket_samples,
        people_detected_samples,
    )


def sample_measurements_between(from_date: datetime, to_date: datetime, verbose=True):
    # Delete the old measurements referred to the mock basket
    db_connection = create_db_connection()
    db_cursor = db_connection.cursor()
    
    db_cursor.execute("DELETE FROM accelerometer_data WHERE basket_id=%s", (MOCK_BASKET_ID,))
    db_cursor.execute("DELETE FROM score_data WHERE basket_id=%s", (MOCK_BASKET_ID,))
    db_cursor.execute("DELETE FROM people_detected_data WHERE basket_id=%s", (MOCK_BASKET_ID,))

    db_cursor.close()
    db_connection.close()

    date = from_date
    while (date <= to_date):
        sample_measurements_for_day(date, verbose)
        date += timedelta(days=1)

    db_connection.commit()


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

        sample_measurements_between(datetime(2015, 1, 1), datetime(2016, 12, 31), verbose=verbose)

    except KeyboardInterrupt as _:
        pass

