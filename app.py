from pickle import FALSE
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import false, true
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "ihazsecretz29445"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_users():
    """Redirect to home page showing users list and add list button."""
    return redirect("/users")
    

@app.route('/users')
def show_users():
    """Home page showing users list and add button."""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Detail page for each user when name is clicked from root route."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route('/users/new', methods=["GET"])
def add_user_form():
    """Show a form to add a user to the database."""
    return render_template("add_user.html")

@app.route('/users/new', methods=["POST"])
def add_user_form_submit():
    """Form to add a user to the database."""
    new_user = User(
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    "Edit an existing user in the database"
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_form(user_id):
    "Handle update form on existing user"

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")