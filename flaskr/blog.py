"""
Blueprint for blog related views.
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    """Index view shows all posts organized by creation date."""
    db = get_db()
    # fetches all the posts from the database
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


#TODO: Create a new view as a base for the create() and update() views.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """View for creating a new post."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title: 
            error = "Title is required."
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Edits a post given its id."""
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

# doesn't use a get method because there is no delete template
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """Deletes a post given its id."""
    post = get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/show')
def show(id):
    post = get_post(id, check_author=False)
    return render_template('blog/show.html', post=post)


def get_post(id, check_author=True):
    """Returns a user post given the post id if the post exists and the request user is post author"""
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if post is None:
        # not found
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post['author_id'] != g.user['id']:
        # forbidden
        abort(403)
    return post
