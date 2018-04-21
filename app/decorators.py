import functools
from flask import session, redirect, url_for


def login_required_(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        return redirect(url_for('main.login'))
    return decorator
