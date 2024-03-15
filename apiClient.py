from sqlalchemy.exc import IntegrityError
import requests
import math
from datetime import datetime
from models import db, Cards


class API:
    def __init__(self):
        self.baseApiURL = "https://api.magicthegathering.io/v1/cards"

    def get_card_info(self, card_id):
        card_url = f"{self.baseApiURL}/{card_id}"
        return requests.get(card_url)

    def full_card_list(self):
        card_url = f"{self.baseApiURL}"
        return requests.get(card_url)

    def get_search_results(self, params, num):
        card_base_url = f"{self.baseApiURL}" + f"?page={num}"
        return requests.get(card_base_url, params=params)

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
        params = {key: value for key, value in search_params.items() if value != ""}
        return params

    def scheduled_job_pages(self):
        card_url = f"{self.baseApiURL}?page=1&pageSize=1"
        results = requests.get(card_url)
        headers = results.headers
        pages = math.ceil(int(headers["Total-Count"]))
        return pages

    def job(self):
        pages = self.scheduled_job_pages()
        for page in range(+pages):
            card_url = f"{self.baseApiURL}?page={page}&pageSize=1"
            results = requests.get(card_url)
            card_info = results.json()["cards"][0]
            # only select cards with a multiverseid otherwise the API will give duplicate cards
            if "multiverseid" in card_info:
                try:
                    card_multiverse_id = card_info["multiverseid"]
                    card_name = card_info["name"]
                    card_img_url = card_info["imageUrl"]
                    card_colors = card_info.get("colors", None)
                    card_type = card_info.get("type", None)
                    card_cmc = card_info.get("cmc", None)
                    card_power = card_info.get("power", None)
                    card_toughness = card_info.get("toughness", None)
                    card_rarity = card_info.get("rarity", None)
                    card_set_name = card_info.get("setName", None)
                    card_text = card_info.get("text", None)
                    card_legalities = card_info.get("legalities", [])
                    card_layout = card_info.get("layout", None)
                    card_rulings = card_info.get("rulings", [])
                    card_id = card_info["id"]
                    new_card = Cards(
                        card_multiverse_id=card_multiverse_id,
                        card_name=card_name,
                        card_img_url=card_img_url,
                        card_colors=card_colors,
                        card_type=card_type,
                        card_cmc=card_cmc,
                        card_power=card_power,
                        card_toughness=card_toughness,
                        card_rarity=card_rarity,
                        card_set_name=card_set_name,
                        card_text=card_text,
                        card_legalities=card_legalities,
                        card_layout=card_layout,
                        card_rulings=card_rulings,
                        card_id=card_id,
                    )
                    db.session.add(new_card)
                    db.session.commit()
                    print("card added to Cards db table")
                except IntegrityError:
                    db.session.rollback()
                    print("Record skipped - already a part of the Cards db table")
                    continue
        print("Job executed at:", datetime.now())
