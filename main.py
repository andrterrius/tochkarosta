import time
from flask import Flask, render_template, url_for, request, session, send_file, redirect, make_response
from jinja2 import Template
from werkzeug.exceptions import HTTPException
from config import *
from psycopg2.extras import DictCursor
import psycopg2
from pymongo import DESCENDING
import datetime

app = Flask(__name__)


def get_news(ip, page):
    news = db.get_news(9, (page-1)*9)
    if news:
        db.add_views_news(ip, 9, (page - 1) * 9)
        return news
    return "error"


def get_events(ip, page):
    events = db.get_events(9, (page-1)*9)
    if news:
        db.add_views_events(ip, 9, (page - 1) * 9)
        return events
    return "error"


def get_general(*args):
    return render_template("index.html", news=get_news(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr), 1), current_page=1, total_pages=db.get_count_news_pages())


@app.route("/")
def index():
    return get_general()


@app.route("/new/<int:id>")
def new_check(id):
    check = db.get_info_new(id)
    if check:
        return render_template("new.html", data=check, page=id)
    return get_general()


@app.route("/news")
def news():
    page = request.args.get("page", 1)
    return render_template("news.html", news=get_news(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr), int(page)), current_page=int(page), total_pages=db.get_count_news_pages())


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/teachers")
def teachers():
    return render_template("teachers.html")


@app.route("/events")
def events():
    page = request.args.get("page", 1)
    return render_template("events.html", events=get_events(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr), int(page)), current_page=int(page), total_pages=db.get_count_events_pages())


@app.route("/event/<int:id>")
def event_check(id):
    check = db.get_info_event(id)
    if check:
        return render_template("event.html", data=check, page=id)
    return get_general()


@app.route("/gallery")
def gallery():
    return render_template("gallery.html", images=db.get_images(10, 0))


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


@app.route("/api/get_images", methods=["POST"])
def get_images():
    try:
        images = db.get_images(10, request.form['offset'])
        if images:
            return {"success": True, "code": Template(template_images).render(images=images), "count": 2}
        return {"error": "Изоображения не найдены"}
    except:
        return {"error": "Ошибка со стороны сервера"}


@app.errorhandler(HTTPException)
def error(error):
    return render_template("error.html", error=error.code)

app.run(debug=True, host='0.0.0.0', port=80)