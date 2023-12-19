"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_CAFE_IMAGE_URL = "/static/images/default-cafe.jpg"
DEFAULT_USER_IMAGE_URL = "/static/images/default-pic.png"


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

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'


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

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

# TEST_USER_DATA = dict(
#     username="test",
#     first_name="Testy",
#     last_name="MacTest",
#     description="Test Description.",
#     email="test@test.com",
#     password="secret",
# )
# {'username': 'test',
#  'first_name': 'Testy',
#  'last_name': 'MacTest',
#  'description': 'Test Description.',
#  'email': 'test@test.com',
#  'password': 'secret'}

# user = User.register(**TEST_USER_DATA)

    @classmethod
    def register(cls, **data):
        """Register user with hashed password and return user."""
        print('data: ', data)

        if len(data['password']) < 6:
            raise ValueError("Too short password")

        hashed = bcrypt.generate_password_hash(data['password']).decode('utf8')

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
                   )

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
