import time

from flask import Flask, render_template, url_for, request, session, send_file, redirect, make_response
from config import *
from psycopg2.extras import DictCursor
import psycopg2
from pymongo import DESCENDING
import datetime
app = Flask(__name__)
def get_news(page):
    news = db.get_news(9, (page-1)*9)
    if news:
        return news
    return "error"

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", news=get_news(1))
@app.route("/new/<int:id>")
def new_check(id):
    check = db.get_info_new(id)
    if check:
        return render_template("news.html", data=check, page=id)
    return redirect(url_for('index'))
@app.route("/news")
def news():
    page = request.args.get("page")
    if page:
        return render_template("news.html", news=get_news(int(page)))
    return "ok"
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/teachers")
def teachers():
    return render_template("teachers.html")
@app.route("/events")
def events():
    return render_template("events.html")
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")
@app.route("/callback")
def callback():
    return render_template("callback.html")
app.run(debug=True, host='0.0.0.0', port=80)