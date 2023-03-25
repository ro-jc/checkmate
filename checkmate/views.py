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

from checkmate.db import get_db


bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/")
def index():
    return redirect(url_for("views.friends"))


@bp.route("/friends")
def friends():
    return render_template("friends.html")


@bp.route("/groups")
def groups():
    return render_template("groups.html")


@bp.route("/starred")
def starred():
    return render_template("starred.html")
