#!/usr/bin/python3
""" Starts a Flask web Application """

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """Home page displays 'Hello HBNB!'"""
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb_display():
    """ Displays 'HBNB' """
    return ("HBNB")


@app.route("/c/<string:text>", strict_slashes=False)
def c_is_fun(text):
    """ Displays C <text> """
    if text:
        text = " ".join(text.split("_"))
        return (f'C {text}')
    return 404


@app.route("/python/", strict_slashes=False)
@app.route("/python/<string:text>", strict_slashes=False)
def python_is_cool(text="is cool"):
    """ Displays Python <text>"""
    text = " ".join(text.split("_"))
    return (f'Python {text}')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
