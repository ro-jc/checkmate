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
from checkmate.forms import UserSearch
from checkmate.functions import get_user_status
from datetime import date

bp = Blueprint("views", __name__, url_prefix="/")


@bp.route("/")
def index():
    if "username" in session:
        db = get_db()

        user = db.users.find_one({"username": session["username"]})
        friends_usernames = user.get("friends", [])
        starred_usernames = user.get("starred", [])
        group_ids = user.get("groups", [])

        friends = db.users.aggregate(
            [
                {"$match": {"username": {"$in": friends_usernames}}},
                {
                    "$project": {
                        "_id": 0,
                        "name": 1,
                        "username": 1,
                        "timetable": {
                            "$arrayElemAt": ["$timetable", date.today().isoweekday()]
                        },
                    }
                },
            ]
        )
        friends = [get_user_status(user) for user in friends]
        starred = [user for user in friends if user["username"] in starred_usernames]
        groups = [i for i in db.groups.find({"id": {"$in": group_ids}})]

        return render_template(
            "index.html", starred=starred, friends=friends, groups=groups
        )

    else:
        return render_template("landing.html")


@bp.route("/requests", methods=["GET", "POST"])
def requests():
    form = UserSearch()
    db = get_db()
    if form.validate_on_submit():
        results = db.users.aggregate(
            [
                {
                    "$project": {
                        "_id": 0,
                        "name": "$name",
                        "username": "$username",
                    }
                },
                {
                    "$match": {
                        "$or": [
                            {"username": {"$regex": form.name.data, "$options": "i"}},
                            {"name": {"$regex": form.name.data, "$options": "i"}},
                        ]
                    }
                },
                {"$sort": {"name": 1}},
                {"$limit": 20},
            ]
        )
        results = [user for user in results]

        return render_template(
            "requests.html", form=form, results=results, show_requests=False
        )

    results = db.users.find_one(
        {"username": session["username"]}, {"_id": 0, "username": 1, "name": 1}
    ).get("requests", [])

    return render_template(
        "requests.html", form=form, results=results, show_requests=True
    )
