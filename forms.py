from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    IntegerField,
    RadioField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, Optional
from mtgsdk import Card, Set, Type, Supertype, Subtype


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])
    profile_image_url = StringField(
        "(Optional) Profile Image URL", validators=[Optional(strip_whitespace=True)]
    )


class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
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

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[Length(min=6)])


class SearchCardsForm(FlaskForm):
    """Card search form"""

    name = StringField("Card Name", validators=[Optional(strip_whitespace=True)])
    set_name = StringField("Set Name", validators=[Optional(strip_whitespace=True)])
    rarity = SelectField(
        "Rarity",
        choices=["", "Common", "Uncommon", "Rare", "Mythic rare"],
        validators=[Optional(strip_whitespace=True)],
    )
    supertypes = SelectField(
        "Supertypes", choices=[""] + Supertype.all(), validators=[Optional()]
    )
    types = SelectField("Types", choices=[""] + Type.all(), validators=[Optional()])
    subtypes = SelectField(
        "Subtypes", choices=[""] + Subtype.all(), validators=[Optional()]
    )
    cmc = IntegerField("Total Mana Cost", validators=[Optional(strip_whitespace=True)])
    colors = RadioField(
        "Colors",
        choices=["White", "Black", "Blue", "Green", "Red"],
        validators=[Optional()],
    )
    power = IntegerField("Power", validators=[Optional(strip_whitespace=True)])
    toughness = IntegerField("Toughness", validators=[Optional(strip_whitespace=True)])
