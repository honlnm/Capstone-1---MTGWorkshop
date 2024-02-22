from flask import (
    render_template,
    flash,
    redirect,
    session,
    g,
)
from sqlalchemy.exc import IntegrityError
from models import db, User
from forms import (
    UserAddForm,
    UserEditForm,
    LoginForm,
)

from flask import Blueprint

user_bp = Blueprint("user", __name__)

CURR_USER_KEY = "curr_user"


@user_bp.before_request
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


@user_bp.route("/signup", methods=["GET", "POST"])
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


@user_bp.route("/login", methods=["GET", "POST"])
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


@user_bp.route("/logout")
def logout():
    """Handle logout of user."""
    do_logout()
    flash("You have successfully logged out.", "success")
    return redirect("/login")


@user_bp.route("/user/<int:user_id>")
def show_user(user_id):
    """Show user profile."""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    return render_template("show_user.html", user=user)


@user_bp.route("/user/edit", methods=["GET", "POST"])
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
            user.location = form.location.data
            user.bio = form.bio.data
            db.session.commit()
            return redirect(f"/user/{user.id}")
        flash("Wrong password, please try again.", "danger")
    return render_template("edit_user.html", form=form, user_id=user.id)


@user_bp.route("/user/delete", methods=["POST"])
def delete_user():
    """Delete user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    do_logout()
    db.session.delete(g.user)
    db.session.commit()
    return redirect("/signup")
