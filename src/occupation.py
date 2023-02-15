from db import create_db_connection
import numpy as np
from math import *
import logging


logger = logging.getLogger("occupation")
#logger.setLevel(getattr(logging, os.environ['LOG_LEVEL'].upper(), None))


def evaluate_occupation(basket_id: int, t):
    """
    Evaluate the occupation probability for a given instant or array of instants `t` based on the measurements stored for the given `basket_id`.

    Parameters:
      - `basket_id`: The basket to evaluate the occupation for
      - `t`: The list of instants in time, expressed as a python `datetime` (in UTC timezone) or as an array of `datetime(s)`,
            for which the occupation should be evaluated

    Returns:
        A single or an array of occupations depending if the input was a scalar or an array
    """

    if not (type(t) == list or type(t) == np.ndarray):
        logger.debug(f"Evaluating the occupation at {t}")
        t = np.array([t])
    else:
        logger.debug(f"Evaluation the occupation on a sequence of {len(t)} time samples starting from {t[0]} ending at {t[-1]}")
    
    t_min, t_max = np.amin(t), np.amax(t)

    # Query data
    db_connection = create_db_connection()

    db_cursor = db_connection.cursor()

    db_cursor.execute("""
        SELECT timestamp FROM accelerometer_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s - INTERVAL 30 MINUTE AND %s
        ORDER BY
            timestamp ASC
    """, (basket_id, t_min, t_max,))
    accelerometer_data = [row[0] for row in db_cursor.fetchall()]

    logger.debug(f"Queried {len(accelerometer_data)} AccelerometerData measurements")

    db_cursor.execute("""
        SELECT timestamp FROM basket_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s - INTERVAL 30 MINUTE AND %s
        ORDER BY
            timestamp ASC
    """, (basket_id, t_min, t_max,))
    basket_data = [row[0] for row in db_cursor.fetchall()]

    logger.debug(f"Queried {len(accelerometer_data)} BasketData measurements")

    db_cursor.execute("""
        SELECT timestamp FROM people_detected_data
        WHERE
            basket_id = %s AND
            timestamp BETWEEN %s - INTERVAL 30 MINUTE AND %s
        ORDER BY
            timestamp ASC
    """, (basket_id, t_min, t_max,))
    people_detected_data = [row[0] for row in db_cursor.fetchall()]

    logger.debug(f"Queried {len(accelerometer_data)} PeopleDetectedData measurements")

    db_cursor.close()
    db_connection.close()

    # Occupation evaluation
    o_t = np.zeros(len(t))

    def evaluate_occupation(t_array, measurement_data, contribution, occupation_array):
        base_idx = 0

        for i, t in enumerate(t_array):
            offset = 0

            while True:
                if (base_idx + offset) >= len(measurement_data):
                    break

                measure_t = measurement_data[base_idx + offset]
                if measure_t > t:
                    # The current measure is more recent, we go on with the next time sample
                    break

                t_delta = t - measure_t
                if t_delta.total_seconds() <= (60 * 30):
                    # If it's within the 30 minutes range, then it could contribute to the final occupation
                    occupation_array[i] += contribution(t, measure_t)
                    offset += 1
                else:
                    base_idx += 1
                    offset = 0

    def probability_curve(t, t0, p, d):
        a = -p / d**2
        b = 0
        c = p

        x = (t - t0).total_seconds()
        y = max(a * (x ** 2) + b * x + c, 0)

        return y

    logger.debug(f"Evaluating occupation contribution from AccelerometerData...")

    evaluate_occupation(t, accelerometer_data, lambda t, event_t: probability_curve(t, event_t, 0.1, 60 * 10), o_t)

    logger.debug(f"Evaluating occupation contribution from BasketData...")

    evaluate_occupation(t, basket_data, lambda t, event_t: probability_curve(t, event_t, 0.4, 60 * 20), o_t)

    logger.debug(f"Evaluating occupation contribution from PeopleDetectedData...")

    evaluate_occupation(t, people_detected_data, lambda t, event_t: probability_curve(t, event_t, 0.06, 60), o_t)

    o_t = np.minimum(o_t, 1)

    logger.debug(f"Evaluated a sequence of {len(o_t)} occupation samples (avg={np.average(o_t)})")

    return o_t[0] if len(o_t) == 1 else o_t.tolist()
