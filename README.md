# Occupation forecaster

This is the service that is responsible to evaluate the occupation of a certain Basket based on its measurements.
It also provides a forecast functionality based on [FbProphet](https://facebook.github.io/prophet/) that tries to predict
the occupation of the Basket for the incoming days.

This project consists of several entrypoints:
- sample_data_generator
- occupation_visualizer
- occupation_forecast_visualizer
- webservice

#### Useful links

- https://facebook.github.io/prophet/docs/quick_start.html
- https://peerj.com/preprints/3190/
- https://nbviewer.jupyter.org/github/nicolasfauchereau/Auckland_Cycling/blob/master/notebooks/Auckland_cycling_and_weather.ipynb
