from datetime import datetime
import pytz
from db import db_connection
import numpy as np
from math import *
import matplotlib.pyplot as plt
from occupation import occupation


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
