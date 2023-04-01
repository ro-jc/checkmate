import functools
import os.path

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from werkzeug.security import generate_password_hash

from checkmate.forms import LoginForm, SignUpForm
from checkmate.db import get_db

from scripts.timetable import create_timetable

bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/login", methods=["POST", "GET"])
def login():
    if "username" in session:
        return redirect(url_for("views.index"))

    form = LoginForm()
    if form.validate_on_submit():
        session["username"] = form.username.data
        return redirect(url_for("views.index"))

    return render_template("login.html", form=form)


@bp.route("/signup", methods=["POST", "GET"])
def signup():
    if "username" in session:
        return redirect(url_for("views.index"))

    form = SignUpForm()
    if form.validate_on_submit():
        get_db().users.insert_one(
            {
                "username": form.username.data,
                "email": form.email.data,
                "password_hash": generate_password_hash(form.password.data),
                "name": form.name.data.title(),
                "timetable": create_timetable(form.timetable.data),
            }
        )

        assets_dir = os.path.join(
            os.path.dirname(current_app.instance_path), 'checkmate/assets'
        )
        avatar = form.avatar.data
        avatar.save(os.path.join(assets_dir, "avatars", form.username.data))

        session["username"] = form.username.data
        return redirect(url_for("views.index"))

    return render_template("signup.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("views.index"))
