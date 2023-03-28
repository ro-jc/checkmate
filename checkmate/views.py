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
        print(friends, starred, groups)
        return render_template(
            "index.html", starred=starred, friends=friends, groups=groups
        )

    else:
        return render_template("landing.html")


@bp.route("/requests", methods=["GET", "POST"])
def requests():
    form = UserSearch()
    if form.validate_on_submit():
        db = get_db()
        username_results = db.users.aggregate(
            [
                {
                    "$project": {
                        "_id": 0,
                        "name": "$name",
                        "username": "$username",
                    }
                },
                {"$match": {"username": {"$regex": form.name.data, "$options": "i"}}},
                {"$sort": {"username": 1}},
                {"$limit": 5},
            ]
        )
        username_results = [user for user in username_results]
        name_results = db.users.aggregate(
            [
                {
                    "$project": {
                        "_id": 0,
                        "name": "$name",
                        "username": "$username",
                    }
                },
                {"$match": {"name": {"$regex": form.name.data, "$options": "i"}}},
                {"$sort": {"name": 1}},
                {"$limit": 15},
            ]
        )
        name_results = [user for user in name_results]

        return render_template(
            "requests.html", form=form, users=username_results + name_results
        )

    return render_template("requests.html", form=form)
