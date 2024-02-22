import os
from flask import (
    Flask,
    render_template,
    redirect,
)
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from routes.user import (
    user_bp,
    contact_bp,
    card_search_bp,
    decks_bp,
    inv_bp,
    wl_bp,
    card_info_bp,
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///mtg_workshop"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.getenv("secret_key")
toolbar = DebugToolbarExtension(app)

app.register_blueprint(user_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(card_search_bp)
app.register_blueprint(decks_bp)
app.register_blueprint(inv_bp)
app.register_blueprint(wl_bp)
app.register_blueprint(card_info_bp)

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()


############## HOMEPAGE & ERROR ROUTES ##############


@app.route("/")
def home():
    """Show home"""
    return redirect("/card-search")


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    return render_template("404.html"), 404
