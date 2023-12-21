"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from mapping import get_map_url

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_CAFE_IMAGE_URL = "/static/images/default-cafe.jpg"
DEFAULT_USER_IMAGE_URL = "/static/images/default-pic.png"
BCRYPT_WORK_FACTOR = 9


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )

    @classmethod
    def get_choices_cities(cls):
        """Create a list of city choices, with each choice as a
        (code, label) tuple.
            E.g. [('berk', 'Berkley'), ('oak', 'Oakland'), ...]
        """
        return [(c.code, c.name) for c in cls.query.order_by('name')]


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default='',
    )

    url = db.Column(
        db.Text,
        nullable=False,
        default='',
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_CAFE_IMAGE_URL,
    )

    city = db.relationship("City", backref='cafes')
    # Backref in Users
    # liking_users = db.relationship(
    #    'User', secondary='cafes_users', backref='liked_cafes')

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'

    def get_map_url(self):
        """Return map url from Google Maps API for cafe."""
        city = self.city
        return get_map_url(self.address, city.name, city.state)


class User(db.Model):
    """User information."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        unique=True,
        nullable=False,
    )

    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
        default='',
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default=DEFAULT_USER_IMAGE_URL,
    )

    hashed_password = db.Column(
        db.Text,
        nullable=False,
    )

    liked_cafes = db.relationship(
        'Cafe', secondary='cafes_users', backref='liking_users')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, **data):
        """Register user with hashed password and return user."""
        print('data: ', data)

        if len(data['password']) < 6:
            raise ValueError("Too short password")

        hashed = bcrypt.generate_password_hash(
            data['password'], BCRYPT_WORK_FACTOR).decode('utf8')

        user = cls(username=data['username'],
                   hashed_password=hashed,
                   first_name=data['first_name'],
                   last_name=data['last_name'],
                   description=data.get('description') or None,
                   email=data['email'],
                   # used data.get b/c TEST_USER_DATA does not have 'image_url'
                   # key -- if there is no 'image_url' key, image_url=None
                   # if signup user with image_url field blank,
                   # data.get('image_url') will be '' which is falsy
                   # then Python will look at the next val, None
                   # now image_url = None
                   image_url=data.get('image_url') or None,
                   admin=data.get('admin') or None,
                   )

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.hashed_password, pwd):
            return u
        else:
            return False


class Like(db.Model):
    """Cafes liked by users."""

    __tablename__ = 'cafes_users'

    liked_cafes = db.Column(
        db.Integer,
        db.ForeignKey('cafes.id'),
        primary_key=True,
    )

    liking_users = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True,
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
