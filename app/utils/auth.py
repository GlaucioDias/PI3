from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if not session.get("logado"):

            flash("Faça login primeiro")

            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated