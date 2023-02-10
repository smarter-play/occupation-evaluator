---
layout: default
---


## Command line

This repository offers several commands that can be mostly used for debug purposes.

---

### sample_data_generator

Fills the database with sample measurements associated to the MockBasket. The measurements are placed between two dates and are generated using probability distributions cheaseled to represent a realistic scenario. The parameters that controls the generation can be found and possibly edited directly on the script.

**Usage:**
```
python3 src/sample_data_generator.py
```

---

### occupation_visualizer

Visualizes the occupation function between two dates for the mock Basket. The occupation is derived based on the measurements.

**Usage:**
```
python3 src/occupation_visualizer.py -b 589505315 -f '2016-08-15 00:00' -t '2016-08-15 23:59'
```

| Parameter | Type | Value |
| --- | --- | --- |
| `--basket`, `-b` | `int` | The ID of the Basket |
| `--from_date`, `-f` | `ISO 8601 date` | The range's initial date |
| `--to_date`, `-f` | `ISO 8601 date` | The range's final date |

---

### occupation_forecast_visualizer

Visualizes the occupation forecast given an history of past measurements for the following days, for a specific Basket.

**Usage:**
```
python3 src/occupation_forecast_visualizer.py -b 589505315 -p '2016-08-01' -np 280 -nf 14 -t '2016-08-07 17:00:00'
```

**Parameters:**
| Parameter | Type | Value |
| --- | --- | --- |
| `--basket`, `-b` | `int` | The ID of the Basket |
| `--present`, `-p` | `ISO 8601 date` | The pivot date after which predict the future |
| `--num_history_days`, `-np` | `int` | The number of days before the `present` date to take as an history |
| `--num_predicted_days`, `-nf` | `int` | The number of days after the `present` date to predict |
| `--t`, `-t` | `ISO 8601 date` | The time (possibly after `present`) to predict the occupation at |

---

### webservice

Starts a web server that permits to other SmartBasket components to make use of the occupation functionalities. The web server configuration can be found in the `.env` file.

**Usage:**

```
python3 src/webservice.py
```

