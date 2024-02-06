from flask_wtf import FlaskForm
from wtforms import widgets
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    IntegerField,
    RadioField,
    SelectField,
    SelectMultipleField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    InputRequired,
)
from mtgsdk import Card, Set, Type, Supertype, Subtype


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(html_tag="ul", prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
    rarity = MultiCheckboxField(
        "Rarity",
        choices=[
            "Common",
            "Uncommon",
            "Rare",
            "Mythic Rare",
        ],
        default=["Common", "Uncommon", "Rare", "Mythic Rare"],
        validators=[InputRequired()],
    )
    supertypes = SelectMultipleField(
        "Supertypes",
        choices=["All Supertypes"] + Supertype.all(),
        default=["All Supertypes"],
        validators=[InputRequired()],
    )
    types = SelectMultipleField(
        "Types",
        choices=["All Types"] + Type.all(),
        default=["All Types"],
        validators=[InputRequired()],
    )
    subtypes = SelectMultipleField(
        "Subtypes",
        choices=["All Subtypes"] + Subtype.all(),
        default=["All Subtypes"],
        validators=[InputRequired()],
    )
    cmc = IntegerField("Total Mana Cost", validators=[Optional(strip_whitespace=True)])
    colors = MultiCheckboxField(
        "Colors",
        choices=["White", "Black", "Blue", "Green", "Red"],
        default=["White", "Black", "Blue", "Green", "Red"],
        validators=[InputRequired()],
    )
    power = StringField("Power", validators=[Optional(strip_whitespace=True)])
    toughness = StringField("Toughness", validators=[Optional(strip_whitespace=True)])
