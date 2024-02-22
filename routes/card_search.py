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

card_search_bp = Blueprint("card_search", __name__)

from forms import (
    SearchCardsForm,
    SelectDeckForm,
)

baseApiURL = "https://api.magicthegathering.io/v1/cards"


@card_search_bp.route("/card-search", methods=["GET", "POST"])
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


@card_search_bp.route("/search-results/page<int:num>", methods=["GET", "POST"])
def view_search_results(num):
    dict = session.get("dict")
    session["result_page"] = num
    dict["page"] = num
    dict["pageSize"] = 100
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
