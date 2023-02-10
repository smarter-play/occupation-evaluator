from occupation_forecast import evaluate_occupation_forecast
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-b", "--basket", type=int, required=True)
    parser.add_argument("-p", "--present", type=datetime.fromisoformat, required=True)
    parser.add_argument("-np", "--num_history_days", type=int, required=True)
    parser.add_argument("-nf", "--num_predicted_days", type=int, required=True)
    parser.add_argument("-t", "--t", type=datetime.fromisoformat, required=True)

    args = parser.parse_args()

    occupation = evaluate_occupation_forecast(
        args.basket,
        args.present,
        args.num_history_days,
        args.num_predicted_days,
        args.t,
        debug=True,
        num_past_days_in_plot=12,
        num_future_days_in_plot=3,
    )

    print(f"Occupation at {args.t} is: {occupation:.2f}")


if __name__ == "__main__":
    main()

