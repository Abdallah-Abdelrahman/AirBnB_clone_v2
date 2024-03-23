#!/usr/bin/python3
'''starts a Flask web application'''
from flask import Flask, render_template


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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    '''python route '''
    return 'Python '+text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    '''number route '''
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def template(n):
    '''template route '''
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_even(n):
    '''template route '''
    return render_template('6-number_odd_or_even.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
