# views/index.py
from flask import render_template
from . import bp  # import the Blueprint instance

@bp.route('/')
def index():
    user = {'name': 'John Doe', 'location': 'Kenya'}
    return render_template('index.html', user=user)
