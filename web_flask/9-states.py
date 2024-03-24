#!/usr/bin/python3
""" Starts a Flask web Application """

from models import storage
from flask import Flask, render_template

app = Flask(__name__)
states = storage.all("State")


@app.route("/states", strict_slashes=False)
def list_state():
    """ list State and their Cities in sorted order """
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """list states with given ID """
    cities = None  # if id is not present, then cities is None
    for state in states.keys():
        if id == state.split(".")[1]:
            cities = states[state]
    return render_template('9-states.html', states_cities=cities)


@app.teardown_appcontext
def teardown(e):
    """ close session """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
