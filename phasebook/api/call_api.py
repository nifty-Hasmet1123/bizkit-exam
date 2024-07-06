from flask import Blueprint, request, jsonify
from phasebook.data.url_data import posts_url, comments_url, users_url, albums_url
import requests

bp = Blueprint("call_api", __name__, url_prefix="/api")

# handler function for the GET only function routes.
def response_handler(response: dict = None, message = None):
    try:
        if response.ok:
            return jsonify(response.json()), 200
        return jsonify({ "error": "Failed to retrieve posts" }), response.status_code
    except (ValueError, TypeError, AttributeError) as exc:
        return jsonify({ "error": message, "status": str(exc) })

# no parameters
@bp.route("my-posts", methods=["GET"])
def get_posts():
    response = requests.get(posts_url, timeout = 90)

    return response_handler(response)

# by url parameter
@bp.route("my-posts/<int:number>", methods=["GET"])
def get_posts_by_id(number):
    if isinstance(number, int) and number:
        new_url = f"{posts_url}/{number}"
        response = requests.get(new_url, timeout = 90)

        return response_handler(response)

# by query parameter
@bp.route("my-comments", methods=["GET"])
def get_comments_by_query_parameter():
    try:
        # should proceed with an error immedietly
        number = request.args.get("number")

        if number and int(number):
            new_url = f"{comments_url}/{number}"
            response = requests.get(new_url, timeout = 90)

            return response_handler(response)
        else:
            return response_handler(message = "no number query parameter provided")
    except (TypeError, ValueError):
        # return jsonify({ "error": "value in number is not integer" })
        return response_handler(message = "value in number query is not integer")

# by post body parameter
@bp.route("my-posts", methods=["POST"])
def post_users_by_body():
    data = request.get_json()
    container = [data.get("userId"), data.get("id"), data.get("title"), data.get("body")]

    if all(value for value in container):
        body_parameter = {
            "userId": container[0],
            "id": container[1],
            "title": container[2],
            "body": container[3]
        }

        response = requests.post(posts_url, json = body_parameter, headers = { "Content-Type": "application/json" })
    
        return response_handler(response)
    
    return jsonify({ "error": "body parameter should have userId, id, title, body" })