from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Song
from forms import RegisterForm, LoginForm, SongForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///djdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "itisasecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def homepage():
  """ add a nav to redirect toute"""
  return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/login")
  
    """Logout route."""



@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)
  
@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/song/new", methods=["GET", "POST"])
def new_song(username):
    """Show add-song form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = SongForm()

    if form.validate_on_submit():
        cover = form.cover.data
        title = form.title.data
        link = form.link.data

        song = Song(
          cover = cover,
          title = title,
          link = link,
          username=username,
        )

        db.session.add(song)
        db.session.commit()

        return redirect(f"/users/{song.username}")

    else:
        return render_template("song/new.html", form=form)
      
@app.route("/song/<int:song_id>/update", methods=["GET", "POST"])
def update_song(song_id):
    """Show update-song form and process it."""

    song = Song.query.get(song_id)

    if "username" not in session or song.username != session['username']:
        raise Unauthorized()

    form = SongForm(obj=song)

    if form.validate_on_submit():
        song.cover = form.cover.data
        song.title = form.title.data
        song.link = form.link.data

        db.session.commit()

        return redirect(f"/users/{song.username}")

    return render_template("/song/edit.html", form=form, song=song)

@app.route("/song/<int:song_id>/delete", methods=["POST"])
def delete_song(song_id):
    """Delete a song."""

    song = Song.query.get(song_id)
    if "username" not in session or song.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(song)
        db.session.commit()

    return redirect(f"/users/{song.username}")