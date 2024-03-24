#!/usr/bin/python3
""" Starts a Flask web Application """

from models import storage
from flask import Flask, render_template
from models.state import State

app = Flask(__name__)
states = storage.all(State)


@app.route("/states_list", strict_slashes=False)
def list_state():
    """ list State and their Cities in sorted order """
    return render_template('7-states_list.html', states=states)


# @app.teardown_appcontext
# def close(e):
#     """ close session """
#     storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
