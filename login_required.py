import functools
from flask import session,redirect,url_for

def login_required(func):
    @functools.wraps(func)
    def wrapper_login_required(*args,**kwargs):
        if session.get("id") is None:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper_login_required
