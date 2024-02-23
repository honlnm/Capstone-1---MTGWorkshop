from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    g,
)

import requests
import math
from models import db, User, CardsOwned, CardWishList
from apiClient import API

card_search_bp = Blueprint("card_search", __name__, url_prefix="/cs")

from forms import (
    SearchCardsForm,
    SelectDeckForm,
)

baseApiURL = "https://api.magicthegathering.io/v1/cards"


def process_form_data(form):
    delimiter = ","
    orDelimiter = "|"
    search_params = {
        "name": form.name.data or "",
        "setName": form.set_name.data or "",
        "rarity": (
            delimiter.join(form.rarity.data) if len(form.rarity.data) != 4 else ""
        ),
        "supertypes": (
            delimiter.join(form.supertypes.data)
            if "All Supertypes" not in form.supertypes.data
            else ""
        ),
        "types": (
            delimiter.join(form.types.data)
            if "All Types" not in form.types.data
            else ""
        ),
        "subtypes": (
            delimiter.join(form.subtypes.data)
            if "All Subtypes" not in form.subtypes.data
            else ""
        ),
        "cmc": form.cmc.data or "",
        "colors": (
            orDelimiter.join(form.colors.data) if len(form.colors.data) != 5 else ""
        ),
        "power": form.power.data or "",
        "toughness": form.toughness.data or "",
    }
    return {key: value for key, value in search_params.items() if value}


@card_search_bp.route("/card-search", methods=["GET", "POST"])
def card_search_function():
    form = SearchCardsForm(request.form)
    if request.method == "GET":
        return render_template("card_search.html", form=form)
    session["dict"] = process_form_data(form)
    return redirect("/cs/search-results/page1")


@card_search_bp.route("/search-results/page<int:num>", methods=["GET", "POST"])
def view_search_results(num):
    dict = session.get("dict")
    card_list = requests.get(baseApiURL, params=dict)
    headers = card_list.headers
    pages = math.ceil(int(headers["Total-Count"]) / 100)
    if g.user:
        user = User.query.get_or_404(g.user.id)
        inventory = CardsOwned.query.filter(CardsOwned.user_id == g.user.id)
        wishlist = CardWishList.query.filter(CardWishList.user_id == g.user.id)
        card_id_inventory_list = [card.card_id for card in inventory]
        card_id_wishlist_list = [card.card_id for card in wishlist]
        form = SelectDeckForm()
        form.set_deck_choices(user_id=g.user.id)
        return render_template(
            "search_results.html",
            user=user,
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


@card_search_bp.route("/card/<int:card_id>", methods=["GET"])
def view_card_info(card_id):
    api = API()
    card = api.get_card_info(card_id)
    card_info = card.json()
    return render_template("card_info.html", card=card_info["card"])
