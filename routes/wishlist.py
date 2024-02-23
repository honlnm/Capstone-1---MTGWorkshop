from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    flash,
    redirect,
    g,
)

from models import db, User, CardsOwned, CardWishList
from apiClient import API

from forms import (
    SelectDeckForm,
    CardQtyEditForm,
)

wl_bp = Blueprint("wish_list", __name__, url_prefix="/wl")


@wl_bp.route("/user/<int:user_id>/wishlist")
def show_wishlist(user_id):
    """Show User Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = User.query.get_or_404(user_id)
    wishlist = CardWishList.query.filter(CardWishList.user_id == g.user.id)
    card_id_wishlist_list = [card.card_id for card in wishlist]
    inventory = CardsOwned.query.filter(CardsOwned.user_id == g.user.id)
    card_id_inventory_list = [card.card_id for card in inventory]
    form = CardQtyEditForm()
    deckForm = SelectDeckForm()
    deckForm.set_deck_choices(user_id=g.user.id)
    return render_template(
        "wishlist.html",
        user=user,
        cards=wishlist,
        wishlist_list=card_id_wishlist_list,
        inventory=inventory,
        inventory_list=card_id_inventory_list,
        form=form,
        deck_form=deckForm,
    )


@wl_bp.route("/user/<int:user_id>/wishlist/<int:card_id>/add", methods=["POST"])
def add_to_wishlist(user_id, card_id):
    """Add Card to Inventory"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        card_check = CardWishList.query.filter(
            CardWishList.user_id == user_id, CardWishList.card_id == card_id
        )
        card_id_list = [card.card_id for card in card_check]
        if card_id in card_id_list:
            card = [CardWishList.query.get_or_404(cardX.id) for cardX in card_check]
            card.card_qty += 1
        else:
            api = API()
            card_detail = api.get_card_info(card_id).json()
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
        return jsonify(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wl_bp.route("/user/<int:user_id>/wishlist/<int:card_id>/adjust-qty", methods=["POST"])
def wishlist_adj_qty(user_id, card_id):
    """Add new deck"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        data = request.json.get("data")
        card = CardWishList.query.filter(
            CardWishList.user_id == int(user_id), CardWishList.card_id == int(card_id)
        )
        for cardX in card:
            cardX.card_qty = data
        db.session.commit()
        return jsonify({"updatedData": cardX.card_qty}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@wl_bp.route("/user/<int:user_id>/wishlist/<int:card_id>/remove", methods=["POST"])
def remove_card_from_wishlist(user_id, card_id):
    """Remove Card from Wish List"""
    if user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    try:
        CardWishList.query.filter(
            CardWishList.user_id == user_id, CardWishList.card_id == card_id
        ).delete()
        db.session.commit()
        return jsonify(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
