import time
from flask import Blueprint

from .data.match_data import MATCHES

bp = Blueprint("match", __name__, url_prefix="/match")


@bp.route("<int:match_id>")
def match(match_id):
    if match_id < 0 or match_id >= len(MATCHES):
        return "Invalid match id", 404

    start = time.time()
    msg = "Match found" if (is_match(*MATCHES[match_id])) else "No match"
    end = time.time()

    return {"message": msg, "elapsedTime": end - start}, 200

def is_match(fave_numbers_1: list, fave_numbers_2: list) -> bool:
    """
    Determines if all number in fave_numbers_2 are present in fave_number_1\n
    Parameters:
            @fave_number_1 (list of integer) -> The list of favorite numbers to check against\n
            @fave_number_2 (list of integer) -> The list of favorite numbers to be checked.\n
    Returns:
        @bool: True if all numbers in fave_numbers_2 exists on fave_numbers_1
    """
    # turns list to set to remove duplicates  
    fave_number_to_set = set(fave_numbers_1)

    # using the all built-in python function that returns true based on the condition.
    return all(number in fave_number_to_set for number in fave_numbers_2)
