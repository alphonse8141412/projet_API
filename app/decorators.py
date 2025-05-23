# app/decorators.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from flask_jwt_extended import jwt_required


def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                return jsonify(msg="Accès refusé : rôle insuffisant"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator







