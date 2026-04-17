# views/contact.py
from flask import render_template
from . import bp  # import the Blueprint instance

@bp.route('/services')
def services():
    return render_template('services.html')
