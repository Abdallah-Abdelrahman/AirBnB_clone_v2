#!/usr/bin/python3
'''starts a Flask web application'''
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''remove the current SQLAlchemy Session after each request
    Args:
        exception:
    '''
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def all_models():
    '''list states, cities, places'''
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template('100-hbnb.html',
                           states=states, amenities=amenities, places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
