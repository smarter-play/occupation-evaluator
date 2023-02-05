from datetime import datetime
import time
import matplotlib.pyplot as plt
from db import db_connection
import numpy as np
from math import *
import pytz


def occupation(basket_id: int, t):
    if np.isscalar(t):
        t = [t]    

    t_min, t_max = np.amin(t), np.amax(t)

    # Query data
    db_cursor = db_connection.cursor()

    db_cursor.execute("""
        SELECT UNIX_TIMESTAMP(timestamp) FROM accelerometer_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN FROM_UNIXTIME(%s) - INTERVAL 30 MINUTE AND FROM_UNIXTIME(%s)
        ORDER BY
            timestamp ASC
    """, (basket_id, t_min, t_max,))
    accelerometer_data = [row[0] for row in db_cursor.fetchall()]

    db_cursor.execute("""
        SELECT UNIX_TIMESTAMP(timestamp) FROM basket_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN FROM_UNIXTIME(%s) - INTERVAL 30 MINUTE AND FROM_UNIXTIME(%s)
        ORDER BY
            timestamp ASC
    """, (basket_id, t_min, t_max,))
    basket_data = [row[0] for row in db_cursor.fetchall()]

    db_cursor.execute("""
        SELECT UNIX_TIMESTAMP(timestamp) FROM people_detected_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN FROM_UNIXTIME(%s) - INTERVAL 30 MINUTE AND FROM_UNIXTIME(%s)
        ORDER BY
            timestamp ASC
    """, (basket_id, t_min, t_max,))
    people_detected_data = [row[0] for row in db_cursor.fetchall()]

    db_cursor.close()

    # Occupation evaluation
    occupation_array = np.zeros(len(t))

    def evaluate_occupation(t_array, measurement_data, contribution, occupation_array):
        base_idx = 0

        for i, t in enumerate(t_array):
            offset = 0

            while True:
                if (base_idx + offset) >= len(measurement_data):
                    #print(f"base_idx {base_idx} + offset {offset} over {len(measurement_data)}")
                    break

                measure_t = measurement_data[base_idx + offset]
                if measure_t > t:
                    # The current measure is more recent, we go on with the next time sample
                    #print(f"measure {datetime.fromtimestamp(measure_t)} > t {datetime.fromtimestamp(t)}")
                    break

                t_delta = t - measure_t
                #print(f"measure {datetime.fromtimestamp(measure_t)} - t {datetime.fromtimestamp(t)} => t_delta {t_delta} ", end='')
                if t_delta <= (60 * 30):
                    # If it's within the 5 minutes range, then it could contribute to the final occupation
                    #print(f"contrib")
                    occupation_array[i] += contribution(t, measure_t)
                    offset += 1
                else:
                    #print(f"going on")
                    base_idx += 1
                    offset = 0

    def probability_curve(t, t0, p, d):
        a = -p / d**2
        b = 0
        c = p

        x = t - t0
        y = max(a * (x ** 2) + b * x + c, 0)

        return y

    evaluate_occupation(t, accelerometer_data, lambda t, event_t: probability_curve(t, event_t, 0.1, 60 * 10), occupation_array)
    evaluate_occupation(t, basket_data, lambda t, event_t: probability_curve(t, event_t, 0.4, 60 * 20), occupation_array)
    evaluate_occupation(t, people_detected_data, lambda t, event_t: probability_curve(t, event_t, 0.06, 60), occupation_array)

    return np.minimum(occupation_array, 1)


def main():
    MOCK_BASKET_ID = 0x23232323

    from_date = datetime(2016, 8, 15, 0, 0, tzinfo=pytz.timezone('UTC'))
    to_date = datetime(2016, 8, 15, 23, 59, tzinfo=pytz.timezone('UTC'))

    db_cursor = db_connection.cursor()

    # Retrieve AccelerometerData
    db_cursor.execute("""
        SELECT UNIX_TIMESTAMP(timestamp) FROM accelerometer_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s AND %s
    """, (MOCK_BASKET_ID, from_date, to_date,))
    accelerometer_data = np.array([row[0] for row in db_cursor.fetchall()])

    # Retrieve BasketData
    db_cursor.execute("""
        SELECT UNIX_TIMESTAMP(timestamp) FROM basket_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s AND %s
    """, (MOCK_BASKET_ID, from_date, to_date,))
    basket_data = np.array([row[0] for row in db_cursor.fetchall()])

    # Retrieve PeopleDetectedData
    db_cursor.execute("""
        SELECT UNIX_TIMESTAMP(timestamp) FROM people_detected_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s AND %s
    """, (MOCK_BASKET_ID, from_date, to_date,))
    people_detected_data = np.array([row[0] for row in db_cursor.fetchall()])

    db_cursor.close()

    # Plot
    from_date_timestamp = from_date.timestamp()
    to_date_timestamp = to_date.timestamp()

    assert((from_date_timestamp <= accelerometer_data).all() and (accelerometer_data <= to_date_timestamp).all())
    assert((from_date_timestamp <= basket_data).all() and (basket_data <= to_date_timestamp).all())
    assert((from_date_timestamp <= people_detected_data).all() and (people_detected_data <= to_date_timestamp).all())

    step_each = 60 * 30  # Each how much time to create a tick
    max_x_ticks = 32
    x_tick_step = max(ceil(((to_date_timestamp - from_date_timestamp) / step_each) / max_x_ticks), 1)
    x_ticks = list(range(
        floor(from_date_timestamp / step_each) * step_each,
        floor(to_date_timestamp / step_each) * step_each + 1,
        (step_each * x_tick_step)
    ))
    x_ticks_labels = [datetime.fromtimestamp(t).strftime("%H:%M") for t in x_ticks]

    fig, ax = plt.subplots(nrows=2, figsize=(16, 6), sharex=True)

    # Measurements plot
    ax[0].scatter(accelerometer_data, np.full(len(accelerometer_data), 0.75), c='r', edgecolor='black', label="Accelerometer data")
    ax[0].scatter(basket_data, np.full(len(basket_data), 0.5), c='b', edgecolor='black', label="Basket data")
    ax[0].scatter(people_detected_data, np.full(len(people_detected_data), 0.25), c='g', edgecolor='black', label="People detection")
    ax[0].set_title(f"{from_date.strftime('%d %b %Y (%a) %H:%m')} → {to_date.strftime('%d %b %Y (%a) %H:%m')}")
    ax[0].set_xlabel("Time")
    ax[0].legend(loc='upper left')
    ax[0].set_xticks(ticks=x_ticks, labels=x_ticks_labels, fontsize=7)

    # Occupation probability plot
    print("Generating occupation probability data...")
    x = np.linspace(from_date_timestamp, to_date_timestamp, 1024)
    y = occupation(MOCK_BASKET_ID, x)

    ax[1].plot(x, y)
    ax[1].set_title("Occupation probability")
    ax[1].set_xlabel("Time")
    ax[1].set_ylim(0, 1.25)
    ax[1].set_xticks(ticks=x_ticks, labels=x_ticks_labels, fontsize=7)

    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()


    


