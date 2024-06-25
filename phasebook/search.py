from flask import Blueprint, request, jsonify

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!
    queries = [
        args.get("id"),
        args.get("name"),
        args.get("age"),
        args.get("occupation")
    ]

    instance = Actions(USERS, *queries)
    result = instance.execute()

    return jsonify(result)

class Actions:
    def __init__(self, data: list, *queries) -> None:
        """
        Initialize the Actions instance with data and optional queries.

        Parameters:
            data: list of user dictionaries to search through.
            *queries: A variable number of query parameters including id, name, age, and occupation.
        """
        self._data = data

        if queries:
            self._user_id, self._name, self._age, self._occupation = queries
        else:
            self._user_id = None
            self._name = None
            self._age = None
            self._occupation = None

    def _if_no_queries(self):
        """
        Check if no queries are provided.

        Returns:
            The full dataset if no queries are provided, else None.
        """
        queries = [ self._user_id, self._name, self._age, self._occupation ]

        if not any(queries):
            return self._data
        return None

    def _filter_users(self):
        """
        Filter users based on the provided queries.

        Returns:
            A list of users that match the query parameters or an error message if an invalid age is provided.
        """
        filtered_users = []

        if self._user_id:
            user_by_id = next((user for user in self._data if user.get("id") == self._user_id), None)
            if user_by_id:
                filtered_users.append(user_by_id)

        if self._name:
            filtered_users.extend([
                user 
                for user in self._data 
                if self._name.lower() in user.get("name", "").lower() and user not in filtered_users
            ])

        if self._age:
            try:
                age = int(self._age)
                filtered_users.extend([
                    user 
                    for user in self._data 
                    if age - 1 <= user.get("age", 0) <= age + 1 and user not in filtered_users
                ])

            except ValueError:
                return {"error": "Invalid age value."}

        if self._occupation:
            filtered_users.extend([
                user 
                for user in self._data 
                if self._occupation.lower() in user.get("occupation", "").lower() and user not in filtered_users
            ])

        return filtered_users

    def execute(self):
        """
        Execute the search based on the provided queries.

        Returns:
            A list of users that match the search parameters, or an error message if an issue occurs.
        """
        try:
            no_queries_result = self._if_no_queries()
            if no_queries_result is not None:
                return no_queries_result
            
            filtered_users = self._filter_users()

            if isinstance(filtered_users, dict) and "error" in filtered_users:
                return filtered_users
            
            if not filtered_users:
                return {"error": "Not found."}
            
            return filtered_users

        except (TypeError, ValueError) as exc:
            return {"error": "check input fields", "stack_trace": str(exc)}