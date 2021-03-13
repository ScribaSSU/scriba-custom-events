from flask import render_template, request, redirect, url_for

from app import app
from settings import vk_conf

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
        return render_template("custom_events.html")
    elif request.method == "POST":  # добавить кастомное событие
        return render_template("add_custom_events.html")


@app.route("/login")
def login():
    return redirect(
        f"https://oauth.vk.com/authorize?client_id={CLIENT_ID}&display=page&redirect_uri={REDIRECTED_URI}&response_type=code"
    )


@app.route("/vk_auth", methods=["GET", "POST"])
def vk_auth():
    if request.method == "GET":
        auth_code = request.args.get("code")
        if not auth_code:
            return redirect(url_for("index"))
        return redirect(
            f"https://oauth.vk.com/access_token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri={REDIRECTED_URI}&code={auth_code}"
        )
    elif request.method == "POST":
        if request.form.get("error"):
            return redirect(url_for("index"))
        access_token = request.form.get("access_token")
        user_id = request.form.get("user_id")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return render_template("index.html")
