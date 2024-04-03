# MTG Workshop
created by Nicole Honl

Link: (https://capstone-1-mtgworkshop.onrender.com)

## About:
The MTG Workshop was built to give Magic the Gathering players the opportunity to build their dream decks without having purchased all the cards they want to use. The site features many search options to find the right card you are looking for and the ability to add any card to your profile's inventory, wish list, or a deck that you've set up. There are many future goals for the website that will be implimented as time goes on. Please feel free to go to the link above (the login) and click the "Demo" button to browse the site as a user.

## Features Implemented:
  - [X] Detailed Card Search
  - [X] Add Cards to Inventory (Cards Owned)
  - [X] Add Cards to Wishlist
  - [X] Create multiple decks
  - [X] Add Cards to created decks

## Future Goals:
  - [ ] Demo User Login
    - [ ] 20 min timeout for Demo User non-activity
  - [ ] Improve loading times by caching data on a regular basis and pulling data from a table vs the api.
  - [ ] Add a link to log Game Data
  - [ ] Have the ability to access Game History
  - [ ] Show said game data statistics in the user profile
    - [ ] Number of wins recorded
    - [ ] Number of Losses recorded
    - [ ] Time Played
  - [ ] Give the user the option to make their profile publically available to view
    - [ ] Would include the option to make certain decks available to view
  - [ ] Make friending and following available
  - [ ] Impliment a life-counter for when playing a game
  - [ ] Option to select deck type and have rules for adding cards
    - Example: Commander, qty 1 of each card.
  - [ ] Provide deck-analytics to show:
    - [ ] Mana bell curve
    - [ ] Number of Cards in the deck
  - [ ] Use an additional API to show up to date, market prices per card
  - [ ] Able to make shopping lists out of wishlists
    - [ ] includes price per card
    - [ ] includes expected shopping total

## Demo:
Instructional Video: [click here](https://youtu.be/fzJ-1mr-eYc)

## How to Clone:
https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

## API Used:
https://magicthegathering.io/#

## Requirements:
- aiohttp==3.9.3
- aiosignal==1.3.1
- APScheduler==3.10.4
- async-timeout==4.0.3
- attrs==23.2.0
- bcrypt==4.1.2
- blinker==1.7.0
- certifi==2024.2.2
- charset-normalizer==3.3.2
- click==8.1.7
- dnspython==2.5.0
- email-validator==2.1.0.post1
- Flask==2.3.3
- Flask-APScheduler==1.12.4
- Flask-Bcrypt==1.0.1
- Flask-DebugToolbar==0.14.1
- Flask-SQLAlchemy==3.1.1
- Flask-WTF==1.2.1
- frozenlist==1.4.1
- greenlet==3.0.1
- gunicorn==21.2.0
- idna==3.6
- itsdangerous==2.1.2
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- mtgsdk==1.3.1
- multidict==6.0.5
- packaging==23.2
- psycopg2-binary==2.9.9
- python-dateutil==2.9.0.post0
- python-dotenv==1.0.0
- pytz==2024.1
- requests==2.31.0
- six==1.16.0
- SQLAlchemy==2.0.23
- SQLAlchemy-Utils==0.41.1
- typing_extensions==4.8.0
- tzlocal==5.2
- urllib3==2.2.0
- Werkzeug==2.3.7
- WTForms==3.1.1
- yarl==1.9.4
