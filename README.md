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

### sample_data_generator

Fills the database with sample measurements associated to a mock Basket. The measurements are placed between two dates (defined within the script) and are generated using probability distributions cheaseled to represent a realistic scenario.

**Usage:**
```
python3 src/sample_data_generator.py
```

---

### occupation_visualizer

Visualizes the occupation function between two dates (defined within the script). The occupation is derived based on the measurements.

**Usage:**
```
python3 src/occupation_visualizer.py
```

---

### occupation_forecast_visualizer

Visualizes the occupation forecast at a certain point in time for the next days (defined within the script).

**Usage:**
```
python3 src/occupation_forecast_visualizer.py
```

---

### webservice

Starts a web server that permits to other SmartBasket components to make use of the occupation functionalities.

**Usage:**
```
python3 src/webservice.py
```

## Useful links

- https://facebook.github.io/prophet/docs/quick_start.html
- https://peerj.com/preprints/3190/
- https://nbviewer.jupyter.org/github/nicolasfauchereau/Auckland_Cycling/blob/master/notebooks/Auckland_cycling_and_weather.ipynb
