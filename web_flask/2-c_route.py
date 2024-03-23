#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    '''hello route '''
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''hbnb route '''
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def txt(text):
    '''text route '''
    return 'C '+text.replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
