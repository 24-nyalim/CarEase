# views/tracking.py
from flask import render_template
from . import bp  # import the Blueprint instance

@bp.route('/tracking')
def tracking():
    return render_template('tracking.html')
