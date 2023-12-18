"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField
# install email_validator if using Email- pip3 install email_validator
from wtforms.validators import InputRequired, Length, URL, Optional


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
        # TODO: make this dynamic list of cities from db
        choices=[
            ("sf", "San Francisco"),
            ("berk", "Berkley"),
            ("oak", "Oakland"),
        ],
    )

    image_url = StringField(
        "Image",
        validators=[Optional(), URL()],
    )
