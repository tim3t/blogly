from asyncio.proactor_events import _ProactorDuplexPipeTransport
from pickle import FALSE
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import false, true
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "ihazsecretz29445"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

"""------Routes redirecting to users and showing user detail information pages------"""

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
    posts = Post.query.filter(Post.user==user_id)
    return render_template("details.html", user=user,posts=posts)



"""-------Routes adding a new user-------"""

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



"""-------Routes editing an existing user's details or deleting an existing user-------"""
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



"""-------Routes for showing, adding, editing, and deleting posts---------"""

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a single post."""

    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)


@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show form for user to add a new post."""

    user = User.query.get_or_404(user_id)
    return render_template("addpost.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_post_form(user_id):
    """Handle new post form for user to add a new post."""

    new_post = Post(
    title = request.form["post_title"],
    content = request.form["post_content"])

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post_form(post_id):
    "Handle update form on existing post"

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes a post."""
    
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/users")

