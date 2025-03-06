from functools import wraps
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify

def role_required(required_role):
    """Decorator to check if the user has the required role."""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            # Get user identity from JWT (username)
            identity = get_jwt_identity()
            
            # Get the role from the JWT claims
            role = identity.get("role")
            
            # If the role doesn't match the required role, return a 403 Forbidden response
            if role != required_role:
                return jsonify({"msg": "Forbidden: You don't have the required role"}), 403
            
            # Otherwise, proceed with the original function
            return fn(*args, **kwargs)
        return wrapper
    return decorator
