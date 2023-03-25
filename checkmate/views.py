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
    return render_template("index.html")
