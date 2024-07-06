from flask import Blueprint
from flask import request, jsonify
import logging

from phasebook.data.schedules import schedules


bp = Blueprint("schedule", __name__, url_prefix="/schedule")

# get the logger configured in the __init__.py file
logger = logging.getLogger(__name__)

@bp.route("<int:user_id>", methods=["GET"])
def schedule(user_id):
    body_paramater = request.get_json()

    start = body_paramater.get("start")
    end = body_paramater.get("end")

    # start and end should have a string/regex pattern that have "HH:MM" numbers
    # check first if the start and end body parameter meets that condition.
    # returns the string format
    # data = check_response(start, end)
    
    # check the user_id in the db memory (via user_id) should only return 1
    user_exists = check_user_id_existence(user_id, schedules)
    concatinated_string = f"{start} - {end}"

    # now check all the time that user have based on the body parameter
    if user_exists:
        new_schedules = user_exists[0]["schedules"]
        

        # add a function here if the schedule is already in the existing
        existence_of_schedule = check_if_schedule_is_existing(new_schedules, concatinated_string)
        
        # log the value
        logger.debug("\nExistence of schedule logs: {}".format(existence_of_schedule))

        # if the string is not yet existing on the schedule this is to avoid duplication
        if not existence_of_schedule:
            new_schedules.append(concatinated_string)

    else:
        # add the user if it is not existing
        data = {
            "user_id": str(user_id),
            "schedules": [ concatinated_string ]
        }

        schedules.append(data)

    return jsonify(schedules)

def check_user_id_existence(user_id: str, schedules):
    # container = []
    
    # for schedule in schedules:
    #     if str(user_id) == schedule["user_id"]:
    #         container.append(schedule)
    #         # break the operation here if the value is found
    #         break
    
    # return container

    return list(filter(lambda schedule: str(user_id) == schedule["user_id"], schedules))

def check_if_schedule_is_existing(schedules, concatinated_string):
    return [
        schedule
        for schedule in schedules
        if concatinated_string == schedule
    ]


# def check_response(start: str = "00:03", end: str = "00:03") -> dict:
#     # maybe first split by colon on each
#     first_start, second_start  = start.split(":")[0], start.split(":")[1]
#     first_end, second_end = end.split(":")[0], end.split(":")[1]

#     return {
#         "first_start": first_start,
#         "second_start": second_start,
#         "first_end": first_end,
#         "second_end": second_end
#     }