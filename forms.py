from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    profile_image_url = StringField('(Optional) Profile Image URL', validators=[Optional(strip_whitespace=True)])

class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    profile_image_url = StringField('(Optional) Image URL', validators=[Optional(strip_whitespace=True)])
    header_image_url = StringField('(Optional) Header Image URL', validators=[Optional(strip_whitespace=True)])
    location = TextAreaField('(Optional) Location', validators=[Optional(strip_whitespace=True)])
    bio = TextAreaField('(Optional) Tell us about yourself', validators=[Optional(strip_whitespace=True)])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])