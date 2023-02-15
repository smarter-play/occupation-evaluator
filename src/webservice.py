from dotenv import load_dotenv


load_dotenv()


import logging
import os


logging.basicConfig(level=getattr(logging, os.environ.get('LOG_LEVEL', "WARNING").upper(), None))


from flask import Flask, request
from datetime import datetime
from occupation import evaluate_occupation
from occupation_forecast import evaluate_occupation_forecast


app = Flask(__name__)


def require_field(name: str):
    if not name in request.args:
        raise ValueError({ 'error': f"Missing required field: \"{name}\"", }, 400)


@app.route("/api/occupation", methods=['GET'])
def occupation():
    try:
        require_field('basket')
        require_field('t')
    except Exception as e:
        return e.args

    basket_id = int(request.args['basket'])
    t = datetime.fromisoformat(request.args['t'])

    o_t = evaluate_occupation(basket_id, t)
    return {
        'occupation': o_t,
        't': t.isoformat(),
    }, 200


@app.route("/api/forecast_occupation", methods=["GET"])
def forecast_occupation():
    try:
        require_field('basket')
        require_field('t')
        require_field('present')
        require_field('num_history_days')
        require_field('num_predicted_days')
    except Exception as e:
        return e.args

    basket_id = int(request.args['basket'])
    present = datetime.fromisoformat(request.args['present'])
    num_history_days = int(request.args['num_history_days'])
    num_predicted_days = int(request.args['num_predicted_days'])
    t = datetime.fromisoformat(request.args['t'])

    o_t = evaluate_occupation_forecast(
        basket_id,
        present,
        num_history_days,
        num_predicted_days,
        t
    )
    return {
        'occupation': o_t,
        't': t.isoformat(),
    }, 200


if __name__ == '__main__':
    app.run(
        host=os.environ["WEBSERVICE_HOST"],
        port=os.environ["WEBSERVICE_PORT"],
    )
