import functools
from flask import session, redirect, url_for, abort
from flask_login import current_user
from .models import Permission


def login_required_(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        return redirect(url_for('main.login'))
    return decorator


def permission_required(permission):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
