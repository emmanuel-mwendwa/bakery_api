from functools import wraps
from flask import abort, g
from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_funtion(*args, **kwargs):
            if not g.current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_funtion
    return decorator