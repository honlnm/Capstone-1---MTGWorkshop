import requests


class API:
    def __init__(self):
        self.baseApiURL = "https://api.magicthegathering.io/v1/cards"

    def get_card_info(self, card_id):
        card_url = f"{self.baseApiURL}/{card_id}"
        return requests.get(card_url)
