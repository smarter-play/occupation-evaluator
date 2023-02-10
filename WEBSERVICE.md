# occupation-forecaster

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
