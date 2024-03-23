#!/usr/bin/python3
'''starts a Flask web application'''
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request
    Args:
        exception:
    '''
    storage.close()


@app.route('/states', strict_slashes=False)
def state():
    '''list statues'''
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    '''get state by id'''
    state = next((s for k, s in storage.all(State).items() if id == s.id), '')
    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
