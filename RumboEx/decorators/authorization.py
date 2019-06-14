from flask import jsonify
from flask_login import login_required

from RumboEx import current_user

# @login_required
def authorize(roles):
    def decorator(function):
        def wrapper(*args, **kwargs):
            global current_user
            try:
                user_role = current_user.object()['roles'][0]
            except:
                return jsonify(Error='User not logged in or has no valid roles'), 402
            for role in roles:
                if user_role == role:
                    return function(*args, **kwargs)
            return jsonify(Error='View not authorized'), 403
        return wrapper
    return decorator