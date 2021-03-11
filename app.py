"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "notverysecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

@app.route('/')
def go_home():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in DB"""
    users = User.query.order_by(User.id).all()
    return render_template('userlist.html', users=users)

@app.route('/users/new')
def add_user_form():
    """Show add user form page"""
    return render_template('createuser.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Process create user form"""
    first = request.form["first name"]
    last = request.form["last name"]
    img = request.form["img url"]

    new_user = User(first_name=first, last_name=last, img_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
   
    return render_template("user.html", user=user , posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show edit user information page"""
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def submit_edit_user(user_id):
    """Process the edit form"""
    first = request.form["first name"]
    last = request.form["last name"]
    img = request.form["img url"]

    user = User.query.get(user_id)
    user.first_name = first
    user.last_name = last
    user.img_url = img
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Show new post form"""
    user = User.query.get_or_404(user_id)
    return render_template("post.html", user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    """Process new post form"""

    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]
    
    new_post = Post(title=title, content=content, user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}" )

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post content"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(post.user_id)
    tags = post.tags

    return render_template("postdetail.html", user=user, post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def show_post_edit(post_id):
    """Show post edit page"""

    post = Post.query.get_or_404(post_id)
    return render_template("editpost.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_post_edit(post_id):
    """Process post edit form"""
    title = request.form['title']
    content = request.form['content']

    post = Post.query.get(post_id)
    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)
    user =  post.user_id
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user}")

@app.route('/tags')
def list_tags():
    """Display list of tags"""
    tags = Tag.query.order_by(Tag.id).all()
    
    return render_template('tagslist.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Display details for selected tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template('tagdetails.html', tag=tag, posts=posts)


@app.route('/tags/new')
def new_tag():
    """Show create tag form"""
    posts = Post.query.all()
    return render_template('createtag.html', posts=posts)


@app.route('/tags/new', methods=["POST"])
def submit_new_tag():
    """Handle submit new tag form"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag = request.form['name']
    new_tag = Tag(name=tag)
    
    db.session.add(new_tag)
    db.session.commit()

    return redirect(f'/tags/{new_tag.id}')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """Show edit tag form"""
    posts = Post.query.all()
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edittag.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def submit_edit_tag(tag_id):
    """Handle submit edit tag form"""
    name = request.form['name']
    tag = Tag.query.get_or_404(tag_id)
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    tag.name = name

    db.session.commit()

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Handle delete tag"""
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
    


