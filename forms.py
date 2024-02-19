from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    IntegerField,
    SelectField,
    SelectMultipleField,
)
from wtforms.validators import InputRequired, Email, Length, Optional, NumberRange
from models import Decks
from mtgsdk import Card, Set, Type, Supertype, Subtype


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ul", prefix_label=False)
    option_widget = widgets.CheckboxInput()


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("E-mail", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    profile_image_url = StringField(
        "(Optional) Profile Image URL", validators=[Optional(strip_whitespace=True)]
    )


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField("Username", validators=[InputRequired()])
    email = StringField("E-mail", validators=[InputRequired(), Email()])
    profile_image_url = StringField(
        "(Optional) Image URL", validators=[Optional(strip_whitespace=True)]
    )
    header_image_url = StringField(
        "(Optional) Header Image URL", validators=[Optional(strip_whitespace=True)]
    )
    location = TextAreaField(
        "(Optional) Location", validators=[Optional(strip_whitespace=True)]
    )
    bio = TextAreaField(
        "(Optional) Tell us about yourself",
        validators=[Optional(strip_whitespace=True)],
    )
    password = PasswordField("Password", validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class AddDeckForm(FlaskForm):
    """Add Deck Form"""

    deck_name = StringField("Deck Name", validators=[InputRequired(), Length(max=30)])


class SelectDeckForm(FlaskForm):
    """Select Deck From Dropdown to add card"""

    deck = SelectField("Add Card to:")

    def set_deck_choices(self, user_id):
        user_decks = Decks.query.filter_by(user_id=user_id).all()
        self.deck.choices = [(deck.id, deck.deck_name) for deck in user_decks]


class DeckEditForm(FlaskForm):
    """Form for editing decks."""

    deck_name = StringField("Deck Name", validators=[InputRequired()])


class CardQtyEditForm(FlaskForm):
    card_qty = IntegerField(
        "Card Qty",
        validators=[
            InputRequired(),
            NumberRange(
                min=1,
                message="Minimum is 1 card. To remove, click the X icon",
            ),
        ],
    )


class SearchCardsForm(FlaskForm):
    """Card search form"""

    name = StringField("Card Name", validators=[Optional(strip_whitespace=True)])
    set_name = StringField("Set Name", validators=[Optional(strip_whitespace=True)])
    rarity = MultiCheckboxField(
        "Rarity",
        choices=[
            "Common",
            "Uncommon",
            "Rare",
            "Mythic",
        ],
        default=["Common", "Uncommon", "Rare", "Mythic"],
    )
    supertypes = SelectMultipleField(
        "Supertypes",
        choices=["All Supertypes"] + Supertype.all(),
        default=["All Supertypes"],
    )
    types = SelectMultipleField(
        "Types",
        choices=["All Types"] + Type.all(),
        default=["All Types"],
    )
    subtypes = SelectMultipleField(
        "Subtypes",
        choices=["All Subtypes"] + Subtype.all(),
        default=["All Subtypes"],
    )
    cmc = IntegerField("Total Mana Cost", validators=[Optional(strip_whitespace=True)])
    colors = MultiCheckboxField(
        "Colors",
        choices=["White", "Black", "Blue", "Green", "Red"],
        default=["White", "Black", "Blue", "Green", "Red"],
    )
    power = StringField("Power", validators=[Optional(strip_whitespace=True)])
    toughness = StringField("Toughness", validators=[Optional(strip_whitespace=True)])
