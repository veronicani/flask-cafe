"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField
# install email_validator if using Email- pip3 install email_validator
from wtforms.validators import InputRequired, Length, URL, Optional, Email


class CafeForm(FlaskForm):
    """Form for adding/editing a cafe."""

    name = StringField(
        "Name",
        validators=[InputRequired(), Length(min=4, max=20)],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    url = StringField(
        "URL",
        validators=[Optional(), URL()],
    )

    address = StringField(
        "Address",
        validators=[InputRequired(), Length(min=4, max=20)],
    )

    city_code = SelectField(
        "City",
    )

    image_url = StringField(
        "Image",
        validators=[Optional(), URL()],
    )


class SignupForm(FlaskForm):
    """Form for user signup."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=4, max=20)],
    )
    
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=1, max=20)],
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()],
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    password = StringField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=20)],
    )

    image_url = StringField(
        "Image",
        validators=[Optional(), URL(), Length(max=255)],
    )


class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField(
        "Username",
        validators=[InputRequired()],
    )

    password = StringField(
        "Password",
        validators=[InputRequired()],
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection."""