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

        friends_usernames = session.get("frineds", [])
        starred_usernames = session.get("starred", [])
        group_ids = session.get("groups", [])

        friends = []
        for username in friends_usernames:
            friends.append(db.users.find_one({"username": username}))

        starred = [user for user in friends if user["username"] in starred_usernames]

        groups = []
        for id in group_ids:
            groups.append(db.groups.find_one({"id": id}))

        return render_template(
            "index.html", starred=starred, friends=friends, groups=groups
        )

    else:
        return render_template("index.html")
