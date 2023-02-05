from db import db_connection
import numpy as np
from math import *


def evaluate_occupation(basket_id: int, t):
    if np.isscalar(t):
        t = [t]

    t_min, t_max = np.amin(t).item(), np.amax(t).item()

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
    o_t = np.zeros(len(t))

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

    evaluate_occupation(t, accelerometer_data, lambda t, event_t: probability_curve(t, event_t, 0.1, 60 * 10), o_t)
    evaluate_occupation(t, basket_data, lambda t, event_t: probability_curve(t, event_t, 0.4, 60 * 20), o_t)
    evaluate_occupation(t, people_detected_data, lambda t, event_t: probability_curve(t, event_t, 0.06, 60), o_t)

    o_t = np.minimum(o_t, 1)

    return o_t[0] if len(o_t) == 1 else o_t.tolist()
