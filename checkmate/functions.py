from datetime import time, datetime


def get_user_status(user):
    user = user.copy()
    timetable = user["timetable"]
    now = datetime.now().time()
    free = True
    done = False
    for i, period in enumerate(timetable):
        period["start"] = time(*period["timings"][:2])
        period["end"] = time(*period["timings"][2:])
        if period["start"] > now:
            break
        if period["end"] > now:
            free = False
            break
    else:
        done = True

    del user["timetable"]

    if not done:
        user["period"] = period
        user["period"]["start"] = period["start"].isoformat()[:-3]
        user["period"]["end"] = period["end"].isoformat()[:-3]

        if i <= len(timetable) - 2:
            timings = timetable[i + 1]["timings"]
            user["next_period_time"] = "%02d:%02d" % (timings[0], timings[1])
    user["free"] = free

    return user
