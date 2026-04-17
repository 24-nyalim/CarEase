# views/about.py
from flask import render_template
from . import bp  # import the Blueprint instance

@bp.route('/progress')
def progress():
    return render_template('progress.html')
