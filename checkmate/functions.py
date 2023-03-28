from datetime import time, datetime


def get_user_status(user):
    user = user.copy()
    timetable = user["timetable"]
    now = datetime.now().time()
    free = True
    done = False
    for i, period in enumerate(timetable):
        print(period)
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
        print(i, len(timetable))
        if i <= len(timetable) - 2:
            user[
                "next_period_time"
            ] = f"{timetable[i + 1]['timings'][0]}:{timetable[i + 1]['timings'][1]}"
    user["free"] = free

    return user
