from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import IntegrityError
import requests
import time
import aiohttp
import asyncio
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

        # split the pages into ranges of 10,000
        # to allow for multiple threads to process the data
        # thus making it faster
        count_start = 0
        page_ranges = []
        for i in range(pages):
            if i % 10_000 == 0 and i != 0:
                page_ranges.append((count_start, i))
                count_start = i + 1
        
        final_page_range = page_ranges[-1][1] + 1, pages + 1
        page_ranges.append(final_page_range)
        return page_ranges

    async def job(self, pages):
        start = time.time()
        async with aiohttp.ClientSession() as session:
            start_page, end_page = pages
            for page in range(start_page, end_page):
                card_url = f"{self.baseApiURL}?page={page}&pageSize=1"
                async with session.get(card_url) as response:
                    if response.status == 200:
                        card_info = await response.json()
                        card_info = card_info["cards"][0]
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
                                # Construct your card object here; ensure this is the correct way for your ORM
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
                                # Assuming you are using a synchronous ORM like SQLAlchemy:
                                db.session.add(new_card)
                                db.session.commit()
                                print("card added to Cards db table")
                            except IntegrityError:
                                db.session.rollback()
                                print("Record skipped - already a part of the Cards db table")
            
            end = time.time()
            print(f"Time taken: {end - start}")

    async def run_job(self):
        pages = self.scheduled_job_pages()
        await asyncio.gather(*(self.job(page_range) for page_range in pages)) 
