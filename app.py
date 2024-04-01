import asyncio
import os
from threading import Thread
from flask import (
    Flask,
    render_template,
    redirect,
    session,
    g,
)
from flask_apscheduler import APScheduler
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from routes.user import user_bp
from routes.card_search import card_search_bp
from routes.decks import decks_bp
from routes.inventory import inv_bp
from routes.wishlist import wl_bp
from datetime import datetime, timedelta, timezone
from apiClient import API

app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///mtg_workshop"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SCHEDULER_API_ENABLED"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.getenv("secret_key")
toolbar = DebugToolbarExtension(app)

app.register_blueprint(user_bp)
app.register_blueprint(card_search_bp)
app.register_blueprint(decks_bp)
app.register_blueprint(inv_bp)
app.register_blueprint(wl_bp)

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()

CURR_USER_KEY = "curr_user"
IDLE_TIMEOUT = timedelta(minutes=15)
scheduler = APScheduler()

############## SCHEDULER ##############


def scheduled_job():
    def start_async_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with app.app_context():
            api = API()
            loop.run_until_complete(api.run_job())
            loop.close()

    thread = Thread(target=start_async_loop)
    thread.start()


def setup_scheduler():
    scheduler.add_job(
        id="scheduled_job",
        func=scheduled_job,
        trigger="interval",
        weeks=1,
        next_run_time=datetime.now(),
    )


with app.app_context():
    setup_scheduler()
    scheduled_job()

scheduler.init_app(app)
scheduler.start()

############## BEFORE RQST ##############


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


############## HOMEPAGE & ERROR ROUTES ##############


@app.route("/")
def home():
    """Show home"""
    return redirect("/cs/card-search")


@app.route("/contact-us")
def contact_us():
    return render_template("contact_us.html")


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    return render_template("404.html"), 404
