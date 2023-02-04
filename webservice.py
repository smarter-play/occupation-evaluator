from flask import Flask, request


app = Flask(__name__)


@app.route("/api/occupation")
def occupation():
    basket = request.args['basket']
    t = request.args['t']
    pass


if __name__ == '__main__':
    pass
