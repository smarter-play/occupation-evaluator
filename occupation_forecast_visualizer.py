from occupation_forecast import evaluate_occupation_forecast
from datetime import datetime


def main():
    MOCK_BASKET_ID = 0x23232323

    present = datetime(2016, 8, 1)
    num_history_days = 100
    num_predicted_days = 14
    t = datetime(2016, 8, 6, 17, 0, 0)

    occupation = evaluate_occupation_forecast(
        MOCK_BASKET_ID,
        present,
        num_history_days,
        num_predicted_days,
        t,
        debug=True
    )

    print(f"Occupation at {t} is: {occupation:.2f}")


if __name__ == "__main__":
    main()

