from flask import render_template, request

from app import app


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/classes", methods=['GET', 'POST'])
def classes():
    if request.method == 'GET':                     # список пар
        return render_template('index.html')
    elif request.method == 'POST':                  # добавить пару
        return render_template('index.html')


@app.route("/events", methods=['GET', 'POST'])
def events():
    if request.method == 'GET':                     # список кастомных событий
        return render_template('index.html')
    elif request.method == 'POST':                  # добавить кастомное событие
        return render_template('index.html')


@app.route("/login")
def login():
    return render_template('index.html')


@app.route("/logout")
def logout():
    return render_template('index.html')
