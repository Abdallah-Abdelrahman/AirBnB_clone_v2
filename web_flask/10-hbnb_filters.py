#!/usr/bin/python3
'''starts a Flask web application'''
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request
    Args:
        exception:
    '''
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def state_city():
    '''list statues and cities'''
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
