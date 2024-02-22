from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    flash,
    redirect,
    session,
    g,
)
from models import db, User, CardsOwned, CardWishList

import requests

from forms import (
    SelectDeckForm,
    CardQtyEditForm,
)

inv_bp = Blueprint("inventory", __name__)

baseApiURL = "https://api.magicthegathering.io/v1/cards"


@inv_bp.route("/user/<int:user_id>/inventory")
def show_inventory(user_id):
    """Show User Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    inventory = CardsOwned.query.filter(CardsOwned.user_id == g.user.id)
    wishlist = CardWishList.query.filter(CardWishList.user_id == g.user.id)
    card_id_inventory_list = [card.card_id for card in inventory]
    card_id_wishlist_list = [card.card_id for card in wishlist]
    form = CardQtyEditForm()
    deckForm = SelectDeckForm()
    deckForm.set_deck_choices(user_id=g.user.id)
    return render_template(
        "inventory.html",
        user=user,
        cards=inventory,
        inventory_list=card_id_inventory_list,
        wishlist_list=card_id_wishlist_list,
        wishlist=wishlist,
        form=form,
        deck_form=deckForm,
    )


@inv_bp.route("/user/<int:user_id>/inventory/<int:card_id>/add", methods=["POST"])
def add_to_inventory(user_id, card_id):
    """Add Card to Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
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
        return jsonify(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inv_bp.route(
    "/user/<int:user_id>/inventory/<int:card_id>/adjust-qty", methods=["POST"]
)
def inv_adj_qty(user_id, card_id):
    """Add new deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        data = request.json.get("data")
        card = CardsOwned.query.filter(
            CardsOwned.user_id == user_id, CardsOwned.card_id == card_id
        )
        for cardX in card:
            cardX.card_qty = data
        db.session.commit()
        return jsonify({"updatedData": cardX.card_qty}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@inv_bp.route("/user/<int:user_id>/inventory/<int:card_id>/remove", methods=["POST"])
def remove_card_from_inventory(user_id, card_id):
    """Remove Card from Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        CardsOwned.query.filter(
            CardsOwned.user_id == user_id, CardsOwned.card_id == card_id
        ).delete()
        db.session.commit()
        return jsonify(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
