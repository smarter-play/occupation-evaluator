from datetime import datetime, timedelta
import pytz
from db import db_connection
import numpy as np
from math import *
import matplotlib.pyplot as plt
from occupation import evaluate_occupation
import pandas as pd
import argparse


def main():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-b", "--basket", type=int, required=True)
    parser.add_argument("-f", "--from_date", type=datetime.fromisoformat, required=True)
    parser.add_argument("-t", "--to_date", type=datetime.fromisoformat, required=True)

    args = parser.parse_args()

    basket_id = args.basket
    from_date = args.from_date
    to_date = args.to_date

    db_cursor = db_connection.cursor()

    # Retrieve AccelerometerData
    db_cursor.execute("""
        SELECT timestamp FROM accelerometer_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s AND %s
    """, (basket_id, from_date, to_date,))
    accelerometer_data = np.array([row[0] for row in db_cursor.fetchall()])

    # Retrieve BasketData
    db_cursor.execute("""
        SELECT timestamp FROM basket_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s AND %s
    """, (basket_id, from_date, to_date,))
    basket_data = np.array([row[0] for row in db_cursor.fetchall()])

    # Retrieve PeopleDetectedData
    db_cursor.execute("""
        SELECT timestamp FROM people_detected_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s AND %s
    """, (basket_id, from_date, to_date,))
    people_detected_data = np.array([row[0] for row in db_cursor.fetchall()])

    db_cursor.close()

    # Plot
    fig, ax = plt.subplots(nrows=2, figsize=(16, 6), sharex=True)

    pd.DataFrame(np.array([accelerometer_data, np.full(len(accelerometer_data), 0.75)]).transpose()) \
        .plot.scatter(ax=ax[0], x=0, y=1, c='r', edgecolor='black', label="Accelerometer data")

    pd.DataFrame(np.array([basket_data, np.full(len(basket_data), 0.5)]).transpose()) \
        .plot.scatter(ax=ax[0], x=0, y=1, c='g', edgecolor='black', label="Basket data")

    pd.DataFrame(np.array([people_detected_data, np.full(len(people_detected_data), 0.25)]).transpose()) \
        .plot.scatter(ax=ax[0], x=0, y=1, c='b', edgecolor='black', label="People detection")

    ax[0].legend(loc='upper left')

    ax[0].set_title(f"{from_date.strftime('%d %b %Y (%a) %H:%m')} → {to_date.strftime('%d %b %Y (%a) %H:%m')}")
    ax[0].set_xlabel("Time")
    ax[0].set_ylim(0, 1)

    t = pd.date_range(from_date, to_date, periods=1028).to_pydatetime()
    occupation_t = evaluate_occupation(basket_id, t)

    pd.DataFrame(np.array([t, occupation_t]).transpose()) \
        .plot(ax=ax[1], x=0, y=1)

    ax[1].set_title("Occupation probability")
    ax[1].set_xlabel("Time")
    ax[1].set_ylim(0, 1.25) 

    fig.tight_layout()
    
    plt.show()


if __name__ == "__main__":
    main()
