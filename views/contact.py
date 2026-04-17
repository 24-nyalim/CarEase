# views/contact.py
from flask import render_template
from . import bp  # import the Blueprint instance

@bp.route('/contact')
def contact():
    return render_template('contact.html')
