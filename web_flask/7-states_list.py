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
    """ list State and their Cities in sorted order """
    # The all_objs is unsorted and contains all classes. value is state name
    state_dict = {k: v.__dict__['name'] for k, v in all_objs.items()
                  if k.split(".")[0] == "State"}
    # The state_name_sort helps sort state using the name of the the state
    state_name_sort = dict(sorted(state_dict.items(),
                                  key=lambda item: item[1]))
    # Since, state_name_sort has been sorted, we now need to have key: value
    # where value is an instance. This means will have sorted all_objs
    sorted_inst_state = {k: all_objs[k] for k in state_name_sort.keys()}

    return render_template('7-states_list.html', states=sorted_inst_state)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
