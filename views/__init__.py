# views/__init__.py
from flask import Blueprint

bp = Blueprint('views', __name__)

# import the view so it gets registered
from . import index
from . import about
from . import services
from . import contact
from . import progress
from . import tracking
