"""Flask App for Flask Cafe."""

import os
from dotenv import load_dotenv

from flask import Flask, render_template, url_for, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cafe, City
from forms import CafeForm

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes
CITY_CODES = [(c.code, c.name) for c in City.query.order_by('name')]

@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=["GET", "POST"])
def add_cafe():
    """ GET: Shows form for adding a cafe.
    POST: Handle adding a cafe and redirects to new cafe's detail page on
    success (flash 'CAFENAME added'). Show form again on failure.
    """

    form = CafeForm()
    form.city_code.choices = CITY_CODES

    if form.validate_on_submit():
        # name = form.name.data
        # description = form.description.data
        # url = form.url.data
        # address = form.address.data
        # city_code = form.city_code.data
        # image_url = form.image_url.data or None

        data = {k: v or None for k, v in form.data.items() if k !=
                "csrf_token"}

        cafe = Cafe(**data)
        # cafe = Cafe(name=form.name.data,
        #             description=form.description.data,
        #             url=form.url.data,
        #             address=form.address.data,
        #             city_code=form.city_code.data,
        #             image_url=form.image_url.data or None)
        db.session.add(cafe)
        db.session.commit()

        flash(f'{cafe.name} added!')
        return redirect(url_for('cafe_detail', cafe_id=cafe.id))
    else:
        return render_template(
            'cafe/add-form.html',
            form=form,
        )


@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    """ GET: Shows form for editing a cafe.
    POST: Handle editing a cafe and redirects to cafe's detail page on
    success (flash 'CAFENAME edited'). Show form again on failure.
    """
    cafe = Cafe.query.get_or_404(cafe_id)
    form = CafeForm(obj=cafe)

    form.city_code.choices = CITY_CODES

    if form.validate_on_submit():
        # NOTE: populate_obj will override db info even if a field is blank
        # TODO: make it so that the populate_obj will pass in None if empty str
        form.populate_obj(cafe)
        # image_url = form.image_url.data or None
        db.session.commit()
        flash(f'{cafe.name} edited!')

        return redirect(url_for('cafe_detail', cafe_id=cafe.id))
    else:
        return render_template(
            'cafe/edit-form.html',
            form=form,
        )