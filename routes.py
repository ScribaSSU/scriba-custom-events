from flask import render_template, request, redirect, url_for

from app import app
from settings import vk_conf
from models.event import find_custom_events
import requests

CLIENT_ID = vk_conf["client_id"]
CLIENT_SECRET = vk_conf["client_secret"]
REDIRECT_URI = vk_conf["redirect_uri"]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/classes", methods=["GET", "POST"])
def classes():
    if request.method == "GET":  # список пар
        return render_template("index.html")
    elif request.method == "POST":  # добавить пару
        return render_template("index.html")


@app.route("/events", methods=["GET", "POST"])
def events():
    if request.method == "GET":  # список кастомных событий
        #Тут надо как-то достать vk_id
        events_list = find_custom_events()
        return render_template("custom_events.html", data=events_list)
    elif request.method == "POST":  # добавить кастомное событие
        return render_template("add_custom_events.html")


@app.route("/login")
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
    access_token = data["access_token"]  # Это все нужно в сессию переделывать
    user_id = data["user_id"]  # Это все нужно в сессию переделывать
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return render_template("index.html")
