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


@app.route('/states/', defaults={'id': None}, strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    '''get state by id'''
    states = storage.all(State)
    state = id

    if id is not None:
        state = next((s for s in storage.all(State).values()
                      if id == s.id), '')

    return render_template('9-states.html', states=states, state=state)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
