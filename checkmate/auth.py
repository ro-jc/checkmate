import functools
from mysql.connector import IntegrityError

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from checkmate.forms import LoginForm
from checkmate.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if True:  # TODO: Check credentials
            # session["username"] = form.username
            return redirect(url_for("views.index"))

    return render_template("login.html", form=form)
