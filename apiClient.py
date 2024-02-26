import requests


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
