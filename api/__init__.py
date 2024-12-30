from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import lissajous
from . import standing_wave
from . import polarized_light
from . import diffraction
from . import wave_superposition 