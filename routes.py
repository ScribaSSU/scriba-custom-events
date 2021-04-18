from datetime import datetime

from flask import render_template, request, redirect, url_for, session

from app import app
from settings import vk_conf
from models.event import Event
from models.user_preferences import UserPreferences
import requests

CLIENT_ID = vk_conf["client_id"]
CLIENT_SECRET = vk_conf["client_secret"]
REDIRECT_URI = vk_conf["redirect_uri"]


@app.route("/")
def index():
    return render_template("index.html",
                           logged_in=session.get("logged_in", False),
                           username=session.get("username"),
                           pfp=session.get("pfp"))


@app.route("/classes_render")
def classes_render():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    return redirect(url_for("classes"))


@app.route("/classes", methods=["GET"])
def classes():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    if request.method == "GET":  # список пар
        preferences = UserPreferences.get_user_group(session.get("user_id", None))
        classes_list = []
        if preferences:
            department = preferences[0].user_department
            group_number = preferences[0].user_group
        else:
            department = ""
            group_number = ""
        departments = {}
        week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        week_types = {"DENOM": "Знаменатель", "NOM": "Числитель"}
        lesson_types = {"LECTURE": "Лекция", "PRACTICE": "Практика"}
        link = "https://scribabot.ml/api/v1.0/departments"
        for d in requests.get(link).json()["departmentsList"]:
            departments[d["url"]] = (d["fullName"], d["shortName"])
        if department and group_number:
            for i in range(1, 7):
                link = "https://scribabot.ml/api/v1.0/schedule/full/" + \
                       f"{department}/{group_number}/{i}"
                classes_list.append(sorted(requests.get(link).json()["lessons"],
                                           key=lambda x: x["lessonTime"]["lessonNumber"]))
        return render_template("classes.html",
                               logged_in=session.get("logged_in", False),
                               username=session.get("username"),
                               pfp=session.get("pfp"),
                               data=classes_list,
                               week_days=week_days,
                               week_types=week_types,
                               lesson_types=lesson_types,
                               departments=departments,
                               user_department=departments[department][1],
                               user_group=group_number)


@app.route("/submit_preferences", methods=["POST"])
def submit_preferences():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    if request.method == "POST":  # добавить кастомное событие
        if request.form.get("submit_preferences"):
            department = request.form.get("department")
            course = request.form.get("course")
            group = request.form.get("group")
            if department and course and group:
                UserPreferences.save_user_group(session["user_id"], department, course, group)
            return redirect(url_for("classes"))
    return redirect(url_for("classes"))


@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_id = request.form.get("event_id")
    Event.delete_event(event_id)
    return redirect(url_for("events"))


def passed_indexes(events_list):
    indexes = []
    now = datetime.now()
    for i, event in enumerate(events_list):
        if event.type_repeat == "Один раз" and event.date_end < now:
            indexes.append(i)

    return indexes


@app.route("/events_render")
def events_render():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    return redirect(url_for("events"))


@app.route("/events", methods=["GET"])
def events():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    if request.method == "GET":  # список кастомных событий
        events_list = Event.find_custom_events(session.get("user_id", None))

        if request.args.get("search_date"):
            search_date = request.args.get("search_date")
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()
            new_list = []
            for event in events_list:

                passed = (search_date - event.date_begin.date()).days
                if passed < 0:
                    continue

                if event.type_repeat == "Один раз" and search_date == event.date_begin.date() or \
                   event.type_repeat == "Раз в неделю" and passed % 7 == 0 or \
                   event.type_repeat == "Раз в две недели" and passed % 14 == 0 or \
                   event.type_repeat == "Ежедневно" or \
                   event.type_repeat == "По будням" and search_date.isoweekday() in range(1, 6):
                   new_list.append(event)

            events_list = new_list

        indexes = passed_indexes(events_list)
        return render_template("custom_events.html",
                               logged_in=session.get("logged_in", False),
                               username=session.get("username"),
                               pfp=session.get("pfp"),
                               data=events_list,
                               indexes=indexes)


@app.route("/add_events_render")
def add_events_render():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    return redirect(url_for("add_events"))


@app.route("/add_events")
def add_events():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    return render_template("add_custom_events.html",
                           logged_in=session.get("logged_in", False),
                           username=session.get("username"),
                           pfp=session.get("pfp"))


@app.route("/submit_events", methods=["POST"])
def submit_events():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    if request.method == "POST":  # добавить кастомное событие
        if request.form.get("submit_event"):
            name_event = request.form.get("name_event")
            description_event = request.form.get("description_event")
            date_begin_event = request.form.get("date_begin_event")
            time_begin_event = request.form.get("time_begin_event")
            if time_begin_event is not None and time_begin_event != '' and \
                    date_begin_event is not None and date_begin_event != '':
                begin_event = date_begin_event + 'T' + time_begin_event
                begin_event = datetime.strptime(begin_event, '%Y-%m-%dT%H:%M')
            date_end_event = request.form.get("date_end_event")
            time_end_event = request.form.get("time_end_event")
            if time_end_event is not None and time_end_event != '' and \
                    date_end_event is not None and date_end_event != '':
                end_event = date_end_event + 'T' + time_end_event
                end_event = datetime.strptime(end_event, '%Y-%m-%dT%H:%M')
            else:
                end_event = begin_event
            type_event = request.form.get("type_event")
            Event.save_event(session["user_id"], name_event,
                             begin_event, end_event,
                             type_event, description_event)
            return redirect(url_for("events"))


@app.route("/login", methods=['POST'])
def login():
    return redirect(
        f"https://oauth.vk.com/authorize?client_id={CLIENT_ID}&display=page&redirect_uri={REDIRECT_URI}&response_type=code"
    )


@app.route("/vk_auth")
def vk_auth():
    auth_code = request.args.get("code")
    if not auth_code:
        return redirect(url_for("index"))
    link = "https://oauth.vk.com/access_token?" + \
           f"client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri={REDIRECT_URI}&code={auth_code}"
    data = requests.get(link).json()
    session["access_token"] = data["access_token"]
    session["user_id"] = data["user_id"]
    session["logged_in"] = True
    link = "https://api.vk.com/method/users.get?" + \
           f"user_ids={session.get('user_id')}&fields=photo_200&access_token={session.get('access_token')}&v=5.130"
    user_data = requests.get(link).json()
    session["username"] = user_data["response"][0]["first_name"]
    session["pfp"] = user_data["response"][0]["photo_200"]
    return redirect(url_for("index"))


@app.route("/logout", methods=['POST'])
def logout():
    session.pop("access_token", None)
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("pfp", None)
    session.pop("logged_in", False)
    return redirect(url_for("index"))