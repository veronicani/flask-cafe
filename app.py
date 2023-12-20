"""Flask App for Flask Cafe."""

import os
from dotenv import load_dotenv

from flask import Flask, render_template, url_for, redirect, flash, session, g
from flask import jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Cafe, City, User
from forms import CafeForm, SignupForm, LoginForm, ProfileEditForm, \
    CSRFProtectForm

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_ECHO'] = True
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)
connect_db(app)
print('SQLALCHEMY_DATABASE_URI: ', app.config['SQLALCHEMY_DATABASE_URI'])

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."
ADMIN_ONLY_MSG = "For administrators only."

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_to_g():
    """Add CSRF form to Flask global."""

    g.form = CSRFProtectForm()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes

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

    If not logged in, redirect to login form with flashed NOT_LOGGED_IN_MSG.
    """
    
    if g.user.admin:

        form = CafeForm()

        form.city_code.choices = City.get_choices_cities()

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

            flash(f'{cafe.name} added!', 'success')
            return redirect(url_for('cafe_detail', cafe_id=cafe.id))

        else:

            return render_template(
                'cafe/add-form.html',
                form=form,
            )

    elif g.user:
        flash(ADMIN_ONLY_MSG, 'danger')
        return redirect(url_for('cafe_list'))

    else:
        flash(NOT_LOGGED_IN_MSG, 'danger')
        return redirect(url_for('login'))


@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    """ GET: Shows form for editing a cafe.
    POST: Handle editing a cafe and redirects to cafe's detail page on
    success (flash 'CAFENAME edited'). Show form again on failure.

    If not logged in, redirect to login form with flashed NOT_LOGGED_IN_MSG.
    """

    if g.user.admin:

        cafe = Cafe.query.get_or_404(cafe_id)
        form = CafeForm(obj=cafe)

        form.city_code.choices = City.get_choices_cities()

        if form.validate_on_submit():
            # NOTE: populate_obj will override db info even if a field is blank
            # TODO: make it so that the populate_obj will pass in None if empty str
            form.populate_obj(cafe)
            # image_url = form.image_url.data or None
            db.session.commit()
            flash(f'{cafe.name} edited!', 'success')

            return redirect(url_for('cafe_detail', cafe_id=cafe.id))
        else:
            return render_template(
                'cafe/edit-form.html',
                form=form,
                cafe=cafe,
            )
        
    elif g.user:
        flash(ADMIN_ONLY_MSG, 'danger')
        return redirect(url_for('cafe_detail', cafe_id=cafe_id))

    else:
        flash(NOT_LOGGED_IN_MSG, 'danger')
        return redirect(url_for('login'))

#######################################
# user signup/login/logout


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ GET: Shows registration form.
    POST: Process registration; if valid, adds user and then log them in. 
        Redirects to cafe list with flashed message “You are signed up and 
        logged in.” If invalid, show form again.
    """

    do_logout()

    form = SignupForm()
    # TODO: no strip whitespace on inputs
    data = {k: v for k, v in form.data.items() if k != "csrf_token"}

    if form.validate_on_submit():

        user = User.register(**data)

        db.session.add(user)

        try:
            db.session.commit()

        except IntegrityError:
            db.session.rollback()

            flash('Username already taken', 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)
        add_user_to_g()
        flash('You are signed up and logged in.', 'success')
        return redirect(url_for('cafe_list'))

    else:
        return render_template(
            'auth/signup-form.html',
            form=form,
        )


@app.route('/login', methods=["GET", "POST"])
def login():
    """ GET: Show login form.
    POST: Process login; if valid, logs user in and redirects to cafe list
        with flashed message “Hello, USERNAME!”. If invalid, show form again.
    """

    form = LoginForm()
    username = form.username.data
    password = form.password.data

    if form.validate_on_submit():

        user = User.authenticate(username, password)

        if user:
            do_login(user)

            flash(f'Hello, {user.username}', 'success')
            return redirect(url_for('cafe_list'))

        else:
            flash("Invalid credentials", 'danger')

    return render_template(
        'auth/login-form.html',
        form=form,
    )


@app.post('/logout')
def logout():
    """ Process logout. Redirects to homepage with flashed message
        “You should have successfully logged out.”
    """

    do_logout()

    flash("You should have successfully logged out.", 'success')
    return redirect(url_for('homepage'))

#######################################
# user profile


@app.get('/profile')
def show_profile():
    """If logged in, show current user's profile.
    If not logged in, redirect to login form with flashed NOT_LOGGED_IN_MSG.
    """

    if g.user:

        return render_template(
            'profile/detail.html',
        )

    else:
        flash(NOT_LOGGED_IN_MSG, 'danger')
        return redirect(url_for('login'))


@app.route('/profile/edit', methods=["GET", "POST"])
def edit_profile():
    """ GET: Show profile edit form if logged in.

    POST: Process profile edit. If valid, redirects to profile page
        with flashed message "Profile edited”. If invalid, show form again.

    If not logged in, redirect to login form with flashed NOT_LOGGED_IN_MSG.
    """

    if g.user:

        form = ProfileEditForm(obj=g.user)         

        if form.validate_on_submit():

            form.populate_obj(g.user)
            db.session.commit()

            flash('Profile edited.', 'success')
            return redirect(url_for('show_profile'))

        else:
            return render_template(
                'profile/edit-form.html',
                form=form,
            )

    else:
        flash(NOT_LOGGED_IN_MSG, 'danger')
        return redirect(url_for('login'))

#######################################
# likes API


@app.get('/api/likes')
def check_if_like():
    """ Determine if the current user likes a cafe.
        Accepts URL query string: "/api/likes?cafe_id=<cafe_id>"
        Returns JSON: {"likes": true|false}

    If not logged in, return JSON: {"error": "Not logged in"}
    """
    
    if g.user:

        cafe_id = int(request.args["cafe_id"])
        user_likes = [cafe.id for cafe in g.user.liked_cafes]
        likes_cafe = cafe_id in user_likes

        return jsonify({"likes": likes_cafe})

    else:

        return jsonify({"error": "Not logged in"})


@app.post('/api/like')
def add_like():
    """ Make the current user like a cafe.
        Accepts JSON: {"cafe_id": <cafe_id (int)>}
        Returns JSON:
            If previously not liked: {"liked": <cafe_id (int)>}
            If already liked: {"error": "Already in likes."}
    If not logged in, return JSON: {"error": "Not logged in"}
    """

    if g.user:

        cafe_id = int(request.json["cafe_id"])
        cafe = Cafe.query.get(cafe_id)
        g.user.liked_cafes.append(cafe)

        try:
            db.session.commit()

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Already in likes."})

        return jsonify({"liked": cafe_id})

    else:

        return jsonify({"error": "Not logged in"})


@app.post('/api/unlike')
def remove_like():
    """ Make the current user unlike a cafe.
        Accepts JSON: {"cafe_id": <cafe_id (int)>}
        Returns JSON:
            If in user's likes: {"unliked": <cafe_id (int)>}
            If not in user's likes: {"error": "Not in your likes."}

    If not logged in, return JSON: {"error": "Not logged in"}
    """

    if g.user:

        cafe_id = int(request.json["cafe_id"])
        cafe = Cafe.query.get(cafe_id)

        try:
            g.user.liked_cafes.remove(cafe)
            db.session.commit()

        except ValueError:
            db.session.rollback()
            return jsonify({"error": "Not in your likes."})

        return jsonify({"unliked": cafe_id})

    else:

        return jsonify({"error": "Not logged in"})