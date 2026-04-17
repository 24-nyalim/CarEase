# views/about.py
from flask import render_template
from . import bp  # import the Blueprint instance

@bp.route('/about')
def about():
    return render_template('about.html')
