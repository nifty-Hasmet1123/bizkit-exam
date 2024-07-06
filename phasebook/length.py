from phasebook.data.match_data import MATCHES
from flask import Blueprint

bp = Blueprint("length", __name__, url_prefix="/length")

@bp.route("")
def length():
    return { "matches_length": len(MATCHES) }
