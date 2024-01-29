from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False)

    password = db.Column(db.Text, nullable=False)

    header_img_url = db.Column(db.Text, default="/static/images/default-header-pic.png")

    profile_img_url = db.Column(db.Text, default="/static/images/default-pic.png")

    location = db.Column(db.Text)

    bio = db.Column(db.Text)

    @classmethod
    def signup(cls, username, email, password, profile_img_url):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            profile_img_url=profile_img_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is auth:
                return user

        return False   

class UserGameData(db.Model):

    __tablename__ = "user_game_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    game_id = db.relationship('GameData', backref="user_game_data")

    user_id = db.relationship('User', backref="user_game_data")

class GameData(db.Model):

    __tablename__ = "game_data"

    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    winner_name = db.Column(db.Text)

    loser_name = db.Column(db.Text)

    time_played = 

    player1 = db.relationship(db.Text, nullable=False)

    player2 = db.Column(db.Text, nullable=False)

    date_played = db.Column(db.Date, nullable=False)

class OwnedCards(db.Model):

    __tablename__ = "cards_owned"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.relationship("User", backref='cards_owned', nullable=False)

    card_id = db.Column(db.Integer, nullable=False)

class CardWishList(db.Model):

    __tablename__ = "card_wishlist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.relationship("User", backref='card_wishlist', nullable=False)

    card_id = db.Column(db.Integer, nullable=False)

class UserDecks(db.Model):

    __tablename__ = "user_decks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    deck_id = db.relationship('Decks', backref='user_decks')

    user_id = db.relationship('User', backref='user_decks')

class Decks(db.Model):

    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    cards

    deck_type

class DeckTypes(db.Model):

    __tablename__ = "deck_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    deck_types  

def connect_db(app):
    db.app = app
    db.init_app(app)