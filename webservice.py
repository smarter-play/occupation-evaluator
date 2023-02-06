from flask import Flask, request
from occupation import evaluate_occupation
from datetime import datetime


app = Flask(__name__)


@app.route("/api/occupation", methods=['GET'])
def occupation():
    if not 'basket' in request.args:
        return { 'error': "Missing required field: \"basket\"", }, 400

    if not 't' in request.args:
        return { 'error': "Missing required field: \"t\"", }, 400

    basket = int(request.args['basket'])
    t = int(request.args['t'])  # Unix timestamp

    o_t = evaluate_occupation(basket, t)
    return {
        'occupation': o_t,
        'datetime': datetime.fromtimestamp(t)
    }, 200


@app.route("/api/occupation_forecast", methods=["GET"])
def occupation_forecast():
    if not 'basket' in request.args:
        return { 'error': "Missing required field: \"basket\"", }, 400

    if not 't' in request.args:
        return { 'error': "Missing required field: \"t\"", }, 400
        
    basket = request.args['basket']
    t = request.args['t']  # Unix timestamp

    o_t = 0
    return {
        'occupation': o_t
    }, 200


if __name__ == '__main__':
    app.run()
