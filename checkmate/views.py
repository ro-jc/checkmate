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
    if "username" in session:
        db = get_db()

        # friends_usernames = session.get("frineds", [])
        # starred_usernames = session.get("starred", [])
        # group_ids = session.get("groups", [])
        user = db.users.find_one({"username": session["username"]})
        friends_usernames = user.get("friends", [])
        starred_usernames = user.get("starred", [])
        group_ids = user.get("groups", [])

        friends = db.users.find({"username": {"$in": friends_usernames}})
        starred = [user for user in friends if user["username"] in starred_usernames]
        groups = db.groups.find({"id": {"$in": group_ids}})

        return render_template(
            "index.html", starred=starred, friends=friends, groups=groups
        )

    else:
        return render_template("landing.html")
