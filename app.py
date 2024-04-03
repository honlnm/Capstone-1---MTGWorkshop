import os
from flask import (
    Flask,
    render_template,
    redirect,
    session,
    g,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_apscheduler import APScheduler
from models import db, connect_db, User
from routes.user import user_bp
from routes.card_search import card_search_bp
from routes.decks import decks_bp
from routes.inventory import inv_bp
from routes.wishlist import wl_bp
from datetime import datetime, timedelta, timezone


app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=20)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL",
    "postgres://zmjjhyfw:4CJMwZnY0tC6TYkrbO7dWEXELvs3aZsj@bubble.db.elephantsql.com/zmjjhyfw",
)
app.config["SCHEDULER_API_ENABLED"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
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
IDLE_TIMEOUT = timedelta(minutes=20)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

############## IDLE TIMEOUT ##############


@app.before_request
def update_session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = IDLE_TIMEOUT
    session.modified = True


@app.before_request
def check_idle_timeout():
    with app.app_context():
        last_activity = session.get("last_activity")
        if last_activity is not None:
            current_time = datetime.now(timezone.utc)
            if (current_time - last_activity) > IDLE_TIMEOUT:
                if g.user and (g.user.email == "demo@example.com"):
                    db.session.delete(g.user)
                    db.session.commit()
                    session.clear()
                    return redirect("/acct/login")
            session["last_activity"] = last_activity.replace(tzinfo=timezone.utc)
        session["last_activity"] = datetime.now(timezone.utc)


scheduler.add_job(
    id="check_idle_timeout", func=check_idle_timeout, trigger="interval", minutes=1
)

############## GLOBAL USER ##############


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
