from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    flash,
    redirect,
    g,
)
from models import db, User, CardsOwned, CardWishList, Decks, DeckCards

from forms import (
    AddDeckForm,
    SelectDeckForm,
    DeckEditForm,
    CardQtyEditForm,
)

from apiClient import API

decks_bp = Blueprint("decks", __name__, url_prefix="/deck")


@decks_bp.route("/user/<int:user_id>/decks")
def show_decks(user_id):
    """Show Deck List"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    decks = Decks.query.filter(Decks.user_id == user_id)
    return render_template("decks.html", decks=decks, user=user)


@decks_bp.route("/user/<int:user_id>/deck/add", methods=["GET", "POST"])
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
        return redirect(f"/deck/user/{g.user.id}/decks")
    return render_template("add_deck.html", form=form)


@decks_bp.route("/user/<int:user_id>/deck/<int:deck_id>")
def show_deck(user_id, deck_id):
    """Show Deck Cards"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    deck = Decks.query.get_or_404(deck_id)
    deck_cards = DeckCards.query.filter(DeckCards.deck_id == deck.id)
    inventory = CardsOwned.query.filter(CardsOwned.user_id == g.user.id)
    wishlist = CardWishList.query.filter(CardWishList.user_id == g.user.id)
    card_id_inventory_list = [card.card_id for card in inventory]
    card_id_wishlist_list = [card.card_id for card in wishlist]
    form = CardQtyEditForm()
    deckForm = SelectDeckForm()
    deckForm.set_deck_choices(user_id=g.user.id)
    return render_template(
        "deck.html",
        user=user,
        cards=deck_cards,
        deck=deck,
        inventory_list=card_id_inventory_list,
        inventory=inventory,
        wishlist_list=card_id_wishlist_list,
        wishlist=wishlist,
        form=form,
        deck_form=deckForm,
    )


@decks_bp.route("/user/<int:user_id>/deck/<int:deck_id>/edit", methods=["GET", "POST"])
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
        return redirect(f"/deck/user/{user.id}/deck/{deck.id}")
    return render_template("edit_deck.html", deck=deck, user=user, form=form)


@decks_bp.route(
    "/user/<int:user_id>/deck/<int:deck_id>/<int:card_id>/adjust-qty",
    methods=["POST"],
)
def deck_card_adj_qty(user_id, deck_id, card_id):
    """Add new deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        data = request.json.get("data")
        card = DeckCards.query.filter(
            DeckCards.deck_id == int(deck_id), DeckCards.card_id == int(card_id)
        )
        for cardX in card:
            cardX.card_qty = data
        db.session.commit()
        return jsonify({"updatedData": cardX.card_qty}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@decks_bp.route("/user/<int:user_id>/deck/<int:deck_id>/delete", methods=["GET"])
def delete_deck(user_id, deck_id):
    """Delete Deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    Decks.query.filter(Decks.id == int(deck_id)).delete()
    db.session.commit()
    return redirect(f"/acct/user/{user.id}")


@decks_bp.route("/user/<int:user_id>/deck/<int:card_id>/add", methods=["POST"])
def add_card_to_deck(user_id, card_id):
    """Add Card to Deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        data = request.json.get("data")
        selected_deck_id = data
        card_check = DeckCards.query.filter(
            DeckCards.deck_id == selected_deck_id, DeckCards.card_id == card_id
        )
        card_id_list = [card.card_id for card in card_check]
        if card_id in card_id_list:
            card = [CardWishList.query.get_or_404(cardX.id) for cardX in card_check]
            card.card_qty += 1
        else:
            api = API()
            card_detail = api.get_card_info(card_id).json()
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
        return jsonify(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@decks_bp.route(
    "/user/<int:user_id>/deck/<int:deck_id>/<int:card_id>/remove", methods=["POST"]
)
def remove_card_from_deck(user_id, deck_id, card_id):
    """Remove Card from Deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        DeckCards.query.filter(
            DeckCards.deck_id == int(deck_id), DeckCards.card_id == int(card_id)
        ).delete()
        db.session.commit()
        return jsonify(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
