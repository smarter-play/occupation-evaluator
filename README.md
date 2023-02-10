# Occupation forecaster

This is the service that is responsible to evaluate the occupation of a certain Basket based on its measurements.
It also provides a forecast functionality based on [FbProphet](https://facebook.github.io/prophet/) that tries to predict
the occupation of the Basket for the incoming days.

## How to install

In order to install and use this service, ensure you have Python3.9 installed. Then, after cloning:

```
python3 -m venv .venv
pip install .
```

Copy `.env.example` to `.env` and initialize its fields, giving connection info and credentials for the DB (that's initialized by [app-backend](https://github.com/smarter-play/app-backend/)).

## How to use

This service is an ensemble of several entrypoints:

#### sample_data_generator

Fills the database with sample measurements associated to a mock Basket. The measurements are placed between two dates (defined within the script) and are generated using probability distributions cheaseled to represent a realistic scenario.

**Usage:**
```
python3 src/sample_data_generator.py
```

---

#### occupation_visualizer

Visualizes the occupation function between two dates for the mock Basket. The occupation is derived based on the measurements.

**Usage:**
```
python3 src/occupation_visualizer.py
```

---

#### occupation_forecast_visualizer

Visualizes the occupation forecast given an history of past measurements for the following days, for the mock Basket.

**Usage:**
```
python3 src/occupation_forecast_visualizer.py --present '2016-08-01' --num_history_days 280 --num_predicted_days 14 --t '2016-08-07 17:00:00'
```

---

#### webservice

Starts a web server that permits to other SmartBasket components to make use of the occupation functionalities.

**Usage:**

```
python3 src/webservice.py
```

## Webservice

```
GET /api/occupation
```

Retrieve the occupation of a Basket at a certain instant in time.

- `basket`: The ID of the basket.
- `t`: The instant in time.

---

```
GET /api/forecast_occupation
```

Forecast the occupation for a Basket at a future instant in time, given measurements history.

- `basket`: The ID of the basket
- `t`: The instant in time where the occupation has to be forecasted.
- `present`: The instant in time after which the forecast has to be made.
- `num_history_days`: The number of days before `present` for which measurements are taken.
- `num_predicted_days`: The number of days in the future to predict.

A wisdom usage expect `t` to be between `present` and `present + num_predicted_days` and `num_history_days` such that `present - num_history_days` was within the period of activity of the Basket.

## Useful links

- https://facebook.github.io/prophet/docs/quick_start.html
- https://peerj.com/preprints/3190/
- https://nbviewer.jupyter.org/github/nicolasfauchereau/Auckland_Cycling/blob/master/notebooks/Auckland_cycling_and_weather.ipynb
