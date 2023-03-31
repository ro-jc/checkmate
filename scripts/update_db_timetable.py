from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

db = MongoClient()["checkmate"]

users = [user for user in db.users.find({}, {"timetable": 1})]

for user in db.users.find():
    for day in user["timetable"]:
        for period in day:
            period["start"] = datetime(2022, 9, 19, *period["timings"][:2])
            period["end"] = datetime(2022, 9, 19, *period["timings"][2:])
            del period["timings"]

    db.users.update_one(
        {"_id": ObjectId(user["_id"])}, {"$set": {"timetable": user["timetable"]}}
    )
