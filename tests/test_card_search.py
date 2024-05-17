from unittest import TestCase

from app import app


app.config['WTF_CSRF_ENABLED'] = False


class TestCardSearch(TestCase):
    def test_redirect_on_bad_data_entry_to_card_search(self):
        """
           Test that the user is redirected to the home
           page if they enter bad data into the search form,
           which would cause the mtg api to return no results.

           The data below is not valid, and will cause the mtg api
           to return a result with no "Total-Count" header.
        """
        with app.test_client() as client:
            with client.session_transaction() as sess:
                # Setting these, as they are set in "card_search_function()"
                # in routes/card_search.py
                sess["dict"] = {
                    "name": "gknsdfkdsf", 
                    "power": "sfgkfsngskgsngskgs", 
                    "rarity": "Common", 
                    "setName": "sgksnfssgsgsg", 
                    "toughness": "sgskngsgksgnsgsgsgsgsgs"
                }

            response = client.get("/cs/search-results/page1", follow_redirects=True)
            html = response.get_data(as_text=True)

            # Indicates a successful response and the presence
            # of the search button, which is present on the home page.
            self.assertIn("card-search-button", html)
            self.assertEqual(response.status_code, 200)
            