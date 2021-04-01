from datetime import datetime

from flask import render_template, request, redirect, url_for, session

from app import app
from settings import vk_conf
from models.event import Event
import requests

CLIENT_ID = vk_conf["client_id"]
CLIENT_SECRET = vk_conf["client_secret"]
REDIRECT_URI = vk_conf["redirect_uri"]


@app.route("/")
def index():
    return render_template("index.html", logged_in=session.get("logged_in", False))


@app.route("/classes", methods=["GET", "POST"])
def classes():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))

    if request.method == "GET":  # список пар
        return render_template("index.html", logged_in=session.get("logged_in", False))
    elif request.method == "POST":  # добавить пару
        return render_template("index.html", logged_in=session.get("logged_in", False))


@app.route('/delete_event', methods=['POST'])
def delete_event():
    event_id = request.form.get("event_id")
    Event.delete_event(event_id)

    return redirect(url_for("events"))


@app.route("/events", methods=["GET", "POST"])
def events():
    if not session.get("logged_in", False):
        return redirect(url_for("index"))
    if request.method == "GET":  # список кастомных событий
        events_list = Event.find_custom_events(session.get("user_id", None))
        return render_template("custom_events.html", logged_in=session.get("logged_in", False), data=events_list)
    elif request.method == "POST":  # добавить кастомное событие
        if request.form.get("submit_event"):
            name_event = request.form.get("name_event")
            description_event = request.form.get("description_event")
            time_begin_event = request.form.get("time_begin_event")
            if time_begin_event is not None and time_begin_event != '':
                time_begin_event = datetime.strptime(time_begin_event, '%Y-%m-%dT%H:%M')
            time_end_event = request.form.get("time_end_event")
            if time_end_event is not None and time_end_event != '':
                time_end_event = datetime.strptime(time_end_event, '%Y-%m-%dT%H:%M')
            else:
                time_end_event = None
            type_event = request.form.get("type_event")
            Event.save_event(session["user_id"], name_event,
                             time_begin_event, time_end_event,
                             type_event, description_event)
            return redirect(url_for("events"))
        else:
            return render_template("add_custom_events.html", logged_in=session.get("logged_in", False))


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
    return redirect(url_for("index"))


@app.route("/logout", methods=['POST'])
def logout():
    session.pop("access_token", None)
    session.pop("user_id", None)
    session.pop("logged_in", False)
    return redirect(url_for("index"))
