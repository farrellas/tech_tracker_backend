from functools import wraps
from flask import request, jsonify

from app.models import User


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return {
                'status': 'error',
                'message': "Missing Header. Please add 'x-access-token' to your Headers."
            }
        if not token:
            return {
                'status': 'error',
                'message': "Missing Auth Token. Please log in to a user that has a valid token."
            }
        user = User.query.filter_by(api_token=token).first()
        if not user:
            return {
                'status': 'error',
                'message': 'That token does not belong to a valid user.'
            }
        return func(user=user, *args, **kwargs)
    return decorated