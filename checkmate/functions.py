import datetime


def get_user_status(user):
    user = user.copy()
    timetable = user["timetable"]
    now = datetime.datetime.now().replace(2022, 9, 19)
    free = True
    done = False
    for i, period in enumerate(timetable):
        if period["start"] > now:
            break
        if period["end"] > now:
            free = False
            break
    else:
        done = True

    if not done:
        user["period"] = period.copy()
        user["period"]["start"] = period["start"].strftime("%H:%M")
        user["period"]["end"] = period["end"].strftime("%H:%M")

        if i <= len(timetable) - 2:
            user["next_period"] = {
                "time": timetable[i + 1]["start"].strftime("%H:%M"),
                "venue": timetable[i + 1]["venue"],
            }

    for period in timetable:
        period["start"] = period["start"].strftime("%H:%M")
        period["end"] = period["end"].strftime("%H:%M")

    user["free"] = free

    return user
