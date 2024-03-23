#!/usr/bin/python3
""" Starts a Flask web Application """

from models import storage
from flask import Flask, render_template

all_objs = storage.all()
app = Flask(__name__)


@app.teardown_appcontext
def close(e):
    """ close session """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def list_state():
    state_dict = {k: v for k, v in all_objs.items()
                  if k.split(".")[0] == "State"}
    return (state_dict)
    sorted_state_dict = dict(sorted(state_dict.items(),
                                    key=lambda item: item[1]))
    return (sorted_state_dict)
    return render_template('7-states_list.html', val=sorted_state_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
