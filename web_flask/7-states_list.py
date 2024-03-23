#!/usr/bin/python3
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state():
    '''list statues'''
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
