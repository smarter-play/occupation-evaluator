
## Occupation forecast

The **Occupation forecast** is the process of forecasting the future occupation based on previous measurements for a specific Basket.

The input of the process are:
- `p`: The instant after which doing the forecast.
- `np`: The number of the past days from which the measurements are taken.
- `nf`: The number of future days to predict.

### Fitting of the prediciton model

The predicition is performed by [FbProphet](https://github.com/facebook/prophet) that is trained on the history.

The history is generated using `p` and `np`: starting from `p` we take a sequence of time samples interspersed of `30min` until `p - np`. Given the time sample sequence, we apply the occupation function and obtain a `{o(t_i)}` sequence which is the history we will use for the prediction.

During the fitting of the model, we want Prophet to be good in grasping the **seasonality** of the occupancy. We assume to have recurrent behavior:
- **Yearly**: low occupancy in late autumn/winter and high occupancy in late-spring/summer. 
- **Weekly**: in the School period, Monday to Saturday days will have low occupancy while Sunday will probably have more occupancy.
- **Daily**: low occupancy at night and high occupancy during the day. 

Obviously we convey Prophet to learn a certain periodical recurrency only if we have enough history data.

It's also very important to hint Prophet that some days are an exception to the recurrent behavior because of the weather. We do such through the **holidays** concept: within the history period and the future period, we mark the days that are considered to be Unplayable.

#### Fitting visualization on fake measurements

<p align="center">
  <img src="/screenshots/occupation_prediction.png" />
</p>

### Inference

After fitting, the prediciton will be a sequence of occupancy values for the next `nf` days starting from `p`, interspersed of `30min`.

Possibly, given a time instant `t^` in the future the final occupancy value is evaluated by interpolating over this sequence in order to approximate `o(t^)`.

<p align="center">
  <img src="/screenshots/occupation_prediction_interp.png" />
</p>
  

