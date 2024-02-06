import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    flash,
    redirect,
    session,
    g,
    abort,
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from models import (
    db,
    connect_db,
    User,
    CardsOwned,
    CardWishList,
    Decks,
    DeckCards,
    DeckTypes,
)
from forms import UserAddForm, UserEditForm, LoginForm, SearchCardsForm
from mtgsdk import Card, Set, Type, Supertype, Subtype
import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///mtg_workshop"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = os.getenv("secret_key")
toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()

baseApiURL = "https://api.magicthegathering.io/v1/cards"

############## USER SIGNUP/LOGIN/LOGOUT ##############


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                profile_image_url=form.profile_image_url.data
                or User.profile_image_url.default.arg,
            )
            db.session.commit()
        except IntegrityError as e:
            flash("Username already taken", "danger")
            return render_template("signup.html", form=form)
        do_login(user)
        return redirect("/")
    else:
        return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        flash("Invalid credentials.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""
    do_logout()
    flash("You have successfully logged out.", "success")
    return redirect("/login")


############## USER ROUTES ##############


@app.route("/user/<int:user_id>")
def show_user(user_id):
    """Show user profile."""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    return render_template("show_user.html", user=user)


@app.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    """Edit user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = g.user
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.profile_image_url = (
                form.profile_image_url.data or "/static/images/default-pic.png"
            )
            user.header_image_url = (
                form.header_image_url.data or "/static/images/default-header-pic.png"
            )
            user.location = form.loction.data
            user.bio = form.bio.data
            db.session.commit()
            return redirect(f"/users/{user.id}")
        flash("Wrong password, please try again.", "danger")
    return render_template("edit_user.html", form=form, user_id=user.id)


@app.route("/user/delete", methods=["POST"])
def delete_user():
    """Delete user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    do_logout()
    db.session.delete(g.user)
    db.session.commit()
    return redirect("/signup")


############## PUBLIC ROUTES ##############


@app.route("/card-search", methods=["GET", "POST"])
def post_card_search_form():
    delimiter = ","
    form = SearchCardsForm()
    if request.method == "GET":
        return render_template("card_search.html", form=form)
    if form.name.data == None:
        card_name = ""
    else:
        card_name = f"{form.name.data}"
    if form.set_name.data == None:
        set_name = ""
    else:
        set_name = form.set_name.data
    if len(form.rarity.data) == 4:
        rarity = ""
    else:
        rarity = delimiter.join(form.rarity.data)
    if "All Supertypes" in form.supertypes.data:
        supertypes = ""
    else:
        supertypes = delimiter.join(form.supertypes.data)
    if "All Types" in form.types.data:
        types = ""
    else:
        types = delimiter.join(form.types.data)
    if "All Subtypes" in form.subtypes.data:
        subtypes = ""
    else:
        subtypes = delimiter.join(form.subtypes.data)
    if form.cmc.data == None:
        cmc = ""
    else:
        cmc = form.cmc.data
    if len(form.colors.data) == 5:
        colors = ""
    else:
        colors = delimiter.join(form.colors.data)
    if form.power.data == None:
        power = ""
    else:
        power = form.power.data
    if form.toughness.data == None:
        toughness = ""
    else:
        toughness = form.toughness.data
    keys = [
        "name",
        "set_name",
        "rarity",
        "supertypes",
        "types",
        "subtypes",
        "cmc",
        "colors",
        "power",
        "toughness",
    ]
    values = [
        card_name,
        set_name,
        rarity,
        supertypes,
        types,
        subtypes,
        cmc,
        colors,
        power,
        toughness,
    ]
    dict = {k: v for (k, v) in zip(keys, values) if v != ""}
    card_list = requests.get(baseApiURL, params=dict)
    return render_template("search_results.html", card_list=card_list.json())


############## GENERAL ROUTES ##############


############## HOMEPAGE & ERROR ROUTES ##############


@app.route("/")
def home():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/signup")
    return redirect("/card-search")


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    return render_template("404.html"), 404
