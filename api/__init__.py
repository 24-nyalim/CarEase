# views/__init__.py
from flask import Blueprint

bp = Blueprint('api', __name__)

# import the view so it gets registered
from . import booking
from . import appointments
from . import daraja
from . import contact
