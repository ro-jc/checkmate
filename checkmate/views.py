from flask import (
    Blueprint,
    current_app,
    send_from_directory,
    render_template,
    request,
    session,
    jsonify,
)

from checkmate.db import get_db
from checkmate.forms import UserSearch
from checkmate.functions import get_user_status
import datetime
from os import listdir

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
                        "friend": {"$in": [session["username"], "$friends"]},
                        "sent_req": {
                            "$in": [session["username"], "$incoming_requests"]
                        },
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
        results = [user for user in results if user["username"] != session["username"]]

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

    return render_template(
        "requests.html", form=form, results=results, show_requests=True
    )


@bp.route("requests/send/<username>")
def request_send(username):
    if username == session["username"]:
        return jsonify({"error": "cannot send request to self"})

    db = get_db()
    db.users.find_one_and_update(
        {"username": session["username"]},
        {"$addToSet": {"outgoing_requests": username}},
    )
    db.users.find_one_and_update(
        {"username": username},
        {"$addToSet": {"incoming_requests": session["username"]}},
    )

    return jsonify({"error": ""})


@bp.route("requests/return", methods=["POST"])
def request_return():
    db = get_db()
    username = request.form["username"]

    if request.form["action"] == "accept":
        db.users.find_one_and_update(
            {"username": session["username"]},
            {
                "$pull": {"incoming_requests": username},
                "$addToSet": {"friends": username},
            },
        )
        db.users.find_one_and_update(
            {"username": username},
            {
                "$pull": {"outgoing_requests": session["username"]},
                "$addToSet": {"friends": session["username"]},
            },
        )
    else:
        db.users.find_one_and_update(
            {"username": session["username"]},
            {"$pull": {"outgoing_requests": username}},
        )

    return jsonify({"error": ""})


@bp.route("/profiles/<username>")
def profile(username):
    db = get_db()
    user = db.users.find_one({"username": username})

    for day in user["timetable"]:
        for period in day:
            period["start"] = period["start"].strftime("%H:%M")
            period["end"] = period["end"].strftime("%H:%M")

    is_friend = session["username"] in user["friends"]

    return render_template("profile.html", user=user, show_full=is_friend)


@bp.route("/assets/avatars/<username>")
def avatar(username):
    if username in listdir(current_app.root_path + "/assets/avatars"):
        return send_from_directory("assets/avatars", username)
    else:
        return send_from_directory("static/images", "user.png")


@bp.route("/themes")
def themes():
    return render_template("themes.html")
