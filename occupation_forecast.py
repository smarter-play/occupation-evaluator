from prophet import Prophet
import pandas as pd
from occupation import evaluate_occupation
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import weather


def forecast_occupation_for_next_days(
    basket_id: int,
    present,
    num_history_days: int,
    num_predicted_days: int,
    **kwargs
):
    """
    Forecast the occupation for a certain basket in the future.

    Parameters:
        - `basket_id`: The ID of the basket for which evaluate the occupation.
        - `present`: The date from which the forecast is performed.
        - `num_history_days`: The number of days prior the `present` date to take data from.
        - `num_predictory_days`: The number of days past the `present` date to predict.

    Keyword parameters:
        - `debug`: Whether to show debug plots.
        - `num_past_days_in_plot`: The number of days prior the `present` date to show on the debug plot.
        - `num_future_days_in_plot`: The number of days past the `present` date to show on the debug plot.

    Returns:
        A 2d-tuple containing the array of future time samples and another array holding respectively their predicted occupancy value
    """

    debug = kwargs.get('debug', False)
    num_past_days_in_plot = kwargs.get('num_past_days_in_plot', 3)
    num_future_days_in_plot = kwargs.get('num_future_days_in_plot', 3)

    num_time_samples = num_history_days * 24 * 2
    
    # Draw time samples starting from the given date back in the past
    print(f"Generating {num_time_samples} time samples with a 30min step...")

    t = pd.date_range(end=present, periods=num_time_samples, freq='30min').to_pydatetime()
    older_date = np.amin(t)
    
    # Evaluate the occupation o(t) for those time samples
    print(f"Generated time samples from {older_date} to {present} ({(present - older_date).days} day(s))")
    
    occupation_t = evaluate_occupation(basket_id, t)

    # Gather (t, o(t)) in a DataFrame so that can be given as an input to FbProphet
    print(f"Predicting {num_predicted_days} days into the future...")

    df = pd.DataFrame(np.array([t, occupation_t]).transpose(), columns = ['ds', 'y'])

    # Define holidays as the days where the weather conditions (or forecasts) aren't suitable for playing
    past_days = df['ds'] \
        .map(lambda date: date.date()) \
        .drop_duplicates() \
        .to_list()
    past_holidays = [day for day in past_days if weather.is_unplayable_day(day)]
    
    future_days = pd.date_range(present + timedelta(days=1), present + timedelta(days=num_predicted_days), freq='1d').to_pydatetime()
    future_holidays = [day.date() for day in future_days if weather.is_unplayable_day(day)]

    holidays = pd.DataFrame({
        'holiday': 'unplayable_day',
        'ds': past_holidays + future_holidays
    })

    # Predict the future!
    model = Prophet(
        growth='flat',
        n_changepoints=round((num_time_samples * 0.8) / (24 * 2)) * 7,
        changepoint_range=0.8,
        yearly_seasonality=44 if (present - older_date) >= timedelta(days=365) else 'auto',
        weekly_seasonality=70 if (present - older_date) >= timedelta(weeks=1) else 'auto',
        daily_seasonality=50 if (present - older_date) >= timedelta(days=1) else 'auto',
        holidays=holidays,
        seasonality_mode='additive',
        #seasonality_prior_scale=6.0,
        #holidays_prior_scale=50.0,
        #changepoint_prior_scale=22.0,
    )
    model.fit(df)
    future = model.make_future_dataframe(periods=(num_predicted_days * 24 * 2), freq='30min')
    prediction = model.predict(future)

    prediction['yhat'].clip(lower=0, upper=1)

    # Plotting
    if debug:
        #model.plot_components(prediction)

        fig, ax = plt.subplots(sharex=True, figsize=(16, 6))

        df[(-num_past_days_in_plot * 24 * 2):] \
            .plot(ax=ax, x='ds', y='y', c='b', label="Data")
        
        true_future_t = pd.date_range(start=present, end=(present + timedelta(days=num_future_days_in_plot)), freq='30min').to_pydatetime()
        true_future_occupation_t = evaluate_occupation(basket_id, true_future_t)

        pd.DataFrame(np.array([true_future_t, true_future_occupation_t]).transpose()) \
            .plot(ax=ax, x=0, y=1, c='g', label="True occupation")

        prediction[((-num_predicted_days - num_past_days_in_plot) * 24 * 2):(((-num_predicted_days + num_future_days_in_plot) * 24 * 2))] \
            .plot(ax=ax, x='ds', y='yhat', c='r', label="Prediction")

        ax.set_ylim(0, 1.25)

        fig.tight_layout()

        plt.show()

    predicted_t = prediction['ds'].dt.to_pydatetime()
    predicted_occupation_t = prediction['yhat']

    return predicted_t[-num_predicted_days * 24 * 2:], predicted_occupation_t[-num_predicted_days * 24 * 2:]


def forecast_occupation(
    basket_id: int,
    present,
    num_history_days: int,
    num_future_days: int,
    t,
    **kwargs
):
    """
    Forecast the occupation for a certain basket at a certain interval in the future.
    
    Parameters:
        - `basket_id`: The ID of the basket for which evaluate the occupation.
        - `present`: The date from which the forecast is performed.
        - `num_history_days`: The number of days prior the `present` date to take data from.
        - `num_predictory_days`: The number of days past the `present` date to predict.
        - `t`: The instant in the future, expressed as a Python `datetime`, where we wish to forecast the occupation.

    Keyword parameters:
        - `debug`: Whether to show debug plots.
        - `num_past_days_in_plot`: The number of days prior the `present` date to show on the debug plot.
        - `num_future_days_in_plot`: The number of days past the `present` date to show on the debug plot.

    Returns:
        A scalar representing the forecasted occupation at the instant `t`.
    """

    debug = kwargs.get('debug', False)

    prediction = forecast_occupation_for_next_days(
        basket_id,
        present,
        num_history_days,
        num_future_days,
        **kwargs
    )

    future_t, future_occupation_t = prediction

    min_future_t = np.amin(future_t)

    # Find the interpolated occupation value at the instant t by shifting the future - predicted - samples
    # and the t to the minimum future date, and scaling the delta to seconds. This is done because `np.interp`
    # can't handle datetime(s) and avoids the usage of UNIX timestamps 
    interpolated_occupation = np.interp(
        (t - min_future_t).total_seconds(),
        [dt.total_seconds() for dt in future_t - min_future_t],
        future_occupation_t
    )

    # Plotting
    if debug:
        fig, ax = plt.subplots()

        pd.DataFrame(np.array([future_t, future_occupation_t]).transpose()) \
            .plot(ax=ax, x=0, y=1, c='orange')
        
        pd.DataFrame(np.array([[t], [interpolated_occupation]]).transpose()) \
            .plot.scatter(ax=ax, x=0, y=1, c='blue')

        ax.set_ylim(0, 1.25)

        fig.tight_layout()

        plt.show()

    return interpolated_occupation

