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
import datetime

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
                            "$arrayElemAt": [
                                "$timetable",
                                {
                                    "$subtract": [
                                        {"$isoDayOfWeek": datetime.datetime.now()},
                                        1,
                                    ]
                                },
                            ]
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

    results = db.users.find_one({"username": session["username"]}).get(
        "incoming_requests", []
    )
    results = [
        db.users.find_one({"username": user}, {"username": 1, "name": 1, "_id": 0})
        for user in results
    ]

    if accept_name := request.form.get("accept_username"):
        db = get_db()
        db.users.find_one_and_update(
            {"username": session["username"]},
            {"$pull": {"incoming_requests": accept_name}},
        )
        db.users.find_one_and_update(
            {"username": session["username"]}, {"$addToSet": {"friends": accept_name}}
        )
        db.users.find_one_and_update(
            {"username": accept_name}, {"$addToSet": {"friends": session["username"]}}
        )

    if req_name := request.form.get("request_username"):
        if not req_name == session["username"]:
            db = get_db()
            db.users.find_one_and_update(
                {"username": req_name},
                {"$addToSet": {"incoming_requests": session["username"]}},
            )

    return render_template(
        "requests.html", form=form, results=results, show_requests=True
    )


@bp.route("/profiles/<username>")
def profile(username):
    db = get_db()
    user = db.find_one({"username": username})

    for day in user["timetable"]:
        for period in day:
            period["start"] = period["start"].strftime("%H:%M")
            period["end"] = period["end"].strftime("%H:%M")

    is_friend = session["username"] in user["friends"]

    return render_template("profile.html", user=user, show_full=is_friend)
