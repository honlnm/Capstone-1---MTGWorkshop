from flask import (
    Blueprint,
    render_template,
)
from apiClient import API
import requests

card_info_bp = Blueprint("card_info", __name__)

baseApiURL = "https://api.magicthegathering.io/v1/cards"


@card_info_bp.route("/card/<int:card_id>", methods=["GET"])
def view_card_info(card_id):
    card = API.get_card_info(card_id)
    card_info = card.json()
    return render_template("card_info.html", card=card_info["card"])
