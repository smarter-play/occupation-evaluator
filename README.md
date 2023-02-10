# Occupation evaluator

A service responsible of evaluating the occupation of a certain Basket based on its measurements.
It also provides a forecast functionality based on [FbProphet](https://facebook.github.io/prophet/) that tries to predict
the occupation of the Basket for the incoming days.

## How to install

In order to install and use this service, ensure you have Python3.9 installed.

Then, after cloning:
```
python3 -m venv .venv
pip install .
```

Copy `.env.example` to `.env` and initialize its fields, giving connection info and credentials for the DB.

In order to use it, you must have a SmartBasket DB instance running (which is managed by [app-backend](https://github.com/smarter-play/app-backend/)).

## How to use

A full list of the functionalities provided by this service, how to access them and even how they're implemented can be found on its [documentation page](https://smarter-play.github.io/occupation-evaluator).

## Useful links

- https://facebook.github.io/prophet/docs/quick_start.html
- https://peerj.com/preprints/3190/
- https://nbviewer.jupyter.org/github/nicolasfauchereau/Auckland_Cycling/blob/master/notebooks/Auckland_cycling_and_weather.ipynb
