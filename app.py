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
from models import db, connect_db, User, CardsOwned, CardWishList, Decks, DeckCards
from forms import (
    UserAddForm,
    UserEditForm,
    LoginForm,
    SearchCardsForm,
    AddDeckForm,
    SelectDeckForm,
    DeckEditForm,
    CardQtyEditForm,
)
import requests
import math

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


############## CONTACT US ROUTE ##############


@app.route("/contact-us")
def contact_us():
    return render_template("contact_us.html")


############## USER ROUTES ##############


@app.route("/user/<int:user_id>")
def show_user(user_id):
    """Show user profile."""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    deck_list = user.decks
    game_list = user.game_data
    return render_template(
        "show_user.html", user=user, decks=deck_list, games=game_list
    )


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
            user.location = form.location.data
            user.bio = form.bio.data
            db.session.commit()
            return redirect(f"/user/{user.id}")
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
    """Full Card Search"""
    delimiter = ","
    form = SearchCardsForm()
    if request.method == "GET":
        return render_template("card_search.html", form=form)
    if form.name.data == None:
        card_name = ""
    else:
        card_name = form.name.data
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
        "setName",
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
    session["dict"] = dict
    return redirect("/search-results/page1")


@app.route("/card/<int:card_id>", methods=["GET"])
def view_card_info(card_id):
    card_url = baseApiURL + "/" + str(card_id)
    card = requests.get(card_url)
    card_info = card.json()
    return render_template("card_info.html", card=card_info["card"], url=card_url)


############## CARD SEARCH RESULTS ##############


@app.route("/search-results/page<int:num>", methods=["GET"])
def view_search_results(num):
    dict = session.get("dict")
    session["result_page"] = num
    dict["page"] = num
    dict["pageSize"] = 100
    card_list = requests.get(baseApiURL, params=dict)
    headers = card_list.headers
    pages = math.ceil(int(headers["Total-Count"]) / 100)
    if g.user:
        inventory = CardsOwned.query.filter(CardsOwned.user_id == g.user.id)
        wishlist = CardWishList.query.filter(CardWishList.user_id == g.user.id)
        card_id_inventory_list = []
        for cardX in inventory:
            card_id_inventory_list.append(cardX.card_id)
        card_id_wishlist_list = []
        for cardX in wishlist:
            card_id_wishlist_list.append(cardX.card_id)
        form = SelectDeckForm()
        form.set_deck_choices(user_id=g.user.id)
        return render_template(
            "search_results.html",
            card_list=card_list.json(),
            inventory=str(card_id_inventory_list),
            wishlist=str(card_id_wishlist_list),
            pagemax=pages,
            currentpage=num,
            pageless=(+num - 1),
            pagelessless=(+num - 2),
            pageplus=(+num + 1),
            pageplusplus=(+num + 2),
            form=form,
        )
    else:
        return render_template(
            "search_results.html",
            card_list=card_list.json(),
            pagemax=pages,
            currentpage=num,
            pageless=(+num - 1),
            pagelessless=(+num - 2),
            pageplus=(+num + 1),
            pageplusplus=(+num + 2),
        )


############## INVENTORY ##############


@app.route("/user/<int:user_id>/inventory")
def show_inventory(user_id):
    """Show User Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    inventory = CardsOwned.query.filter(CardsOwned.user_id == user.id)
    wishlist = CardWishList.query.filter(CardWishList.user_id == user_id)
    form = CardQtyEditForm()
    return render_template(
        "inventory.html", user=user, cards=inventory, wishlist=wishlist, form=form
    )


@app.route("/user/<int:user_id>/inventory/<int:card_id>/add")
def add_to_inventory(user_id, card_id):
    """Add Card to Inventory"""
    num = session["result_page"]
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    card_check = CardsOwned.query.filter(
        CardsOwned.user_id == user_id, CardsOwned.card_id == card_id
    )
    card_id_list = []
    for cardX in card_check:
        card_id_list.append(cardX.card_id)
    if card_id in card_id_list:
        card = ""
        for cardX in card_check:
            card = CardsOwned.query.get_or_404(cardX.id)
        card.card_qty += 1
    else:
        card_detail = requests.get(baseApiURL + "/" + str(card_id)).json()
        card = card_detail["card"]
        new_card = CardsOwned(
            user_id=user_id,
            card_id=card_id,
            card_qty=int("1"),
            card_name=card["name"],
            card_img=card["imageUrl"],
            card_colors=card.get("colors", None),
            card_type=card["type"],
            card_cmc=card.get("cmc", None),
            card_power=card.get("power", None),
            card_toughness=card.get("toughness", None),
        )
        db.session.add(new_card)
    db.session.commit()
    return redirect(f"/search-results/page{num}")


@app.route(
    "/user/<int:user_id>/inventory/<int:card_id>/adjust-qty", methods=["GET", "POST"]
)
def inv_adj_qty(user_id, card_id):
    """Add new deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = CardQtyEditForm()
    if form.validate_on_submit():
        print(user_id + "," + card_id)
        card = CardsOwned.query.filter(
            CardsOwned.user_id == int(user_id), CardsOwned.card_id == int(card_id)
        )
        for cardX in card:
            cardX.card_qty = form.card_qty.data
            db.session.commit()
        return redirect(f"/user/{g.user.id}")
    return redirect(f"/user/{user_id}/inventory")


@app.route("/user/<int:user_id>/inventory/<int:card_id>/remove")
def remove_card_from_inventory(user_id, card_id):
    """Remove Card from Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    CardsOwned.query.filter(
        CardsOwned.user_id == int(user_id), CardsOwned.card_id == int(card_id)
    ).delete()
    db.session.commit()
    return redirect(f"/user/{user_id}/inventory")


############## WISHLIST ##############


@app.route("/user/<int:user_id>/wishlist")
def show_wishlist(user_id):
    """Show User Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    wishlist = CardWishList.query.filter(CardWishList.user_id == user.id)
    inventory = CardsOwned.query.filter(CardsOwned.user_id == user_id)
    return render_template(
        "wishlist.html", user=user, cards=wishlist, inventory=inventory
    )


@app.route("/user/<int:user_id>/wishlist/<int:card_id>/add")
def add_to_wishlist(user_id, card_id):
    """Add Card to Inventory"""
    num = session["result_page"]
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    card_check = CardWishList.query.filter(
        CardWishList.user_id == user_id, CardWishList.card_id == card_id
    )
    card_id_list = []
    for cardX in card_check:
        card_id_list.append(cardX.card_id)
    if card_id in card_id_list:
        card = ""
        for cardX in card_check:
            card = CardWishList.query.get_or_404(cardX.id)
        card.card_qty += 1
    else:
        card_detail = requests.get(baseApiURL + "/" + str(card_id)).json()
        card = card_detail["card"]
        new_card = CardWishList(
            user_id=user_id,
            card_id=card_id,
            card_qty=int("1"),
            card_name=card["name"],
            card_img=card["imageUrl"],
            card_colors=card.get("colors", None),
            card_type=card["type"],
            card_cmc=card.get("cmc", None),
            card_power=card.get("power", None),
            card_toughness=card.get("toughness", None),
        )
        db.session.add(new_card)
    db.session.commit()
    return redirect(f"/search-results/page{num}")


@app.route("/user/<int:user_id>/wishlist/<int:card_id>/remove")
def remove_card_from_wishlist(user_id, card_id):
    """Remove Card from Wish List"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    CardWishList.query.filter(
        CardWishList.user_id == int(user_id), CardWishList.card_id == int(card_id)
    ).delete()
    db.session.commit()
    return redirect(f"/user/{user_id}/wishlist")


############## DECKS ##############


@app.route("/user/<int:user_id>/decks")
def show_decks(user_id):
    """Show Deck List"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    decks = Decks.query.filter(Decks.user_id == user_id)
    return render_template("decks.html", decks=decks, user=user)


@app.route("/user/<int:user_id>/deck/add", methods=["GET", "POST"])
def add_deck(user_id):
    """Add new deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = AddDeckForm()
    if form.validate_on_submit():
        new_deck = Decks(deck_name=form.deck_name.data, user_id=g.user.id)
        db.session.add(new_deck)
        db.session.commit()
        flash(f"{new_deck.deck_name} has been added to your deck list!")
        return redirect(f"/user/{g.user.id}")
    return render_template("add_deck.html", form=form)


@app.route("/user/<int:user_id>/deck/<int:deck_id>")
def show_deck(user_id, deck_id):
    """Show Deck Cards"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    deck = Decks.query.get_or_404(deck_id)
    deck_cards = DeckCards.query.filter(DeckCards.deck_id == deck.id)
    inventory = CardsOwned.query.filter(CardsOwned.user_id == user_id)
    wishlist = CardWishList.query.filter(CardWishList.user_id == user_id)
    return render_template(
        "deck.html",
        user=user,
        cards=deck_cards,
        deck=deck,
        inventory=inventory,
        wishlist=wishlist,
    )


@app.route("/user/<int:user_id>/deck/<int:deck_id>/edit", methods=["GET", "POST"])
def edit_deck(user_id, deck_id):
    """Edit Deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    deck = Decks.query.get_or_404(deck_id)
    form = DeckEditForm(obj=deck)
    if form.validate_on_submit():
        deck.deck_name = form.deck_name.data
        db.session.commit()
        return redirect(f"/user/{user.id}/deck/{deck.id}")
    return render_template("edit_deck.html", deck=deck, user=user, form=form)


@app.route("/user/<int:user_id>/deck/<int:deck_id>/delete", methods=["GET"])
def delete_deck(user_id, deck_id):
    """Delete Deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    Decks.query.filter(Decks.id == int(deck_id)).delete()
    db.session.commit()
    return redirect(f"/user/{user.id}")


@app.route("/user/<int:user_id>/deck/<int:card_id>/add", methods=["POST"])
def add_card_to_deck(user_id, card_id):
    """Add Card to Deck"""
    num = session["result_page"]
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    form = SelectDeckForm(request.form)
    form.set_deck_choices(user_id)
    selected_deck_id = form.deck.data
    card_check = DeckCards.query.filter(
        DeckCards.deck_id == selected_deck_id, DeckCards.card_id == card_id
    )
    card_id_list = []
    for cardX in card_check:
        card_id_list.append(cardX.card_id)
    if card_id in card_id_list:
        card = ""
        for cardX in card_check:
            card = DeckCards.query.get_or_404(cardX.id)
        card.card_qty += 1
    else:
        card_detail = requests.get(baseApiURL + "/" + str(card_id)).json()
        card = card_detail["card"]
        new_card = DeckCards(
            deck_id=selected_deck_id,
            card_id=card_id,
            card_qty=int("1"),
            card_name=card["name"],
            card_img=card["imageUrl"],
            card_colors=card.get("colors", None),
            card_type=card["type"],
            card_cmc=card.get("cmc", None),
            card_power=card.get("power", None),
            card_toughness=card.get("toughness", None),
        )
        db.session.add(new_card)
    db.session.commit()
    return redirect(f"/search-results/page{num}")


@app.route("/user/<int:user_id>/deck/<int:deck_id>/<int:card_id>/remove")
def remove_card_from_deck(user_id, deck_id, card_id):
    """Remove Card from Deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    DeckCards.query.filter(
        DeckCards.deck_id == int(deck_id), DeckCards.card_id == int(card_id)
    ).delete()
    db.session.commit()
    return redirect(f"/user/{user_id}/deck/{deck_id}")


############## CARDS ##############


@app.route("/card/<int:cardmultiverseid>")
def show_card_info():
    """Show Card Info (Public)"""


############## HOMEPAGE & ERROR ROUTES ##############


@app.route("/")
def home():
    """Show home"""
    return redirect("/card-search")


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    return render_template("404.html"), 404
