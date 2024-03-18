from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    g,
)
import math
from models import User, CardsOwned, CardWishList
from apiClient import API

card_search_bp = Blueprint("card_search", __name__, url_prefix="/cs")

from forms import (
    SearchCardsForm,
    SelectDeckForm,
)


@card_search_bp.route("/card-search", methods=["GET", "POST"])
def card_search_function():
    form = SearchCardsForm(request.form)
    if request.method == "GET":
        return render_template("card_search.html", form=form)
    api = API()
    session["dict"] = api.process_form_data(form)
    return redirect("/cs/search-results/page1")


def pages_of_100(results):
    headers = results.headers
    pages = math.ceil(int(headers["Total-Count"]) / 100)
    return pages


@card_search_bp.route("/search-results/page<int:num>", methods=["GET", "POST"])
def view_search_results(num):
    params = session.get("dict")
    api = API()
    card_list = api.get_search_results(params, num)
    pages = pages_of_100(card_list)
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
    if g.user:
        user = User.query.get_or_404(g.user.id)
        inventory = CardsOwned.query.filter(CardsOwned.user_id == g.user.id)
        wishlist = CardWishList.query.filter(CardWishList.user_id == g.user.id)
        card_id_inventory_list = [card.card_id for card in inventory]
        card_id_wishlist_list = [card.card_id for card in wishlist]
        form = SelectDeckForm()
        form.set_deck_choices(user_id=g.user.id)
        return render_template(
            "card_info.html",
            card=card_info["card"],
            user=user,
            inventory=str(card_id_inventory_list),
            wishlist=str(card_id_wishlist_list),
            form=form,
        )
    return render_template("card_info.html", card=card_info["card"])
