from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy(session_options={"expire_on_commit": False})


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    header_image_url = db.Column(
        db.Text, default="/static/images/default-header-pic.png"
    )
    profile_image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    location = db.Column(db.Text)
    bio = db.Column(db.Text)
    game_data = db.relationship("GameData")
    cards_owned = db.relationship("CardsOwned")
    card_wishlist = db.relationship("CardWishList")
    decks = db.relationship("Decks")

    @classmethod
    def signup(cls, username, email, password, profile_image_url):
        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")
        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            profile_image_url=profile_image_url,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False


class GameData(db.Model):
    __tablename__ = "game_data"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_title = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    winner_name = db.Column(db.Text)
    loser_name = db.Column(db.Text)
    sec_duration = db.Column(db.Integer)
    player1 = db.Column(db.Text, nullable=False)
    player2 = db.Column(db.Text, nullable=False)
    date_played = db.Column(db.Date, nullable=False)


class CardsOwned(db.Model):
    __tablename__ = "cards_owned"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    card_id = db.Column(db.Integer, nullable=False)
    card_qty = db.Column(db.Integer, nullable=False)
    card_name = db.Column(db.Text, nullable=False)
    card_img = db.Column(db.Text, nullable=False)
    card_colors = db.Column(db.Text)
    card_type = db.Column(db.Text, nullable=False)
    card_cmc = db.Column(db.Integer)
    card_power = db.Column(db.Integer)
    card_toughness = db.Column(db.Integer)


class CardWishList(db.Model):
    __tablename__ = "card_wish_list"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    card_id = db.Column(db.Integer, nullable=False)
    card_qty = db.Column(db.Integer, nullable=False)
    card_name = db.Column(db.Text, nullable=False)
    card_img = db.Column(db.Text, nullable=False)
    card_colors = db.Column(db.Text)
    card_type = db.Column(db.Text, nullable=False)
    card_cmc = db.Column(db.Integer)
    card_power = db.Column(db.Integer)
    card_toughness = db.Column(db.Integer)


class Decks(db.Model):
    __tablename__ = "decks"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    deck_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"))
    cards = db.relationship("DeckCards", backref="decks")


class DeckCards(db.Model):
    __tablename__ = "deck_cards"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("decks.id", ondelete="cascade"))
    card_id = db.Column(db.Integer, nullable=False)
    card_qty = db.Column(db.Integer, nullable=False)
    card_name = db.Column(db.Text, nullable=False)
    card_img = db.Column(db.Text, nullable=False)
    card_colors = db.Column(db.Text)
    card_type = db.Column(db.Text, nullable=False)
    card_cmc = db.Column(db.Integer)
    card_power = db.Column(db.Integer)
    card_toughness = db.Column(db.Integer)


############## CONNECT DB ##############


def connect_db(app):
    db.app = app
    db.init_app(app)
