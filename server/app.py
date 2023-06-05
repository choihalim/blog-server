#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request
from flask_restful import Resource

# Local imports
from config import app, db, api
from models import User, Post, Comment, Follower

# Views go here!
@app.route('/')
def index():
    return f'<h1>Blogging Platform</h1>'

@app.route('/login')
def login():
    return f'<h1>Login Page</h1>'

@app.route('/create_account')
def create_account():
    return f'<h1>Create Account Page</h1>'

@app.route('/search')
def search_empty():
    return f'<h1>Search Page</h1>'

@app.route('/search/<string:parameter>')
def search(parameter):
    return f'<h1>Search Page</h1>'

@app.route('/<string:user>')
def user_page(user):
    return f"<h1>{user.username}'s Page</h1>"

@app.route('/<string:user>/<int:post_id>')
def user_post_page(user, post_id):
    return f"<h1>{user.username}'s Page</h1>"

@app.route('/<string:user>/following')
def following(user):
    return f"<h1>{user.username}'s Following Page</h1>"

@app.route('/<string:user>/followers')
def followers(user):
    return f"<h1>{user.username}'s Followers Page</h1>"

@app.route('/<string:user>/create')
def create_post(user):
    return f"<h1>Post New Blog</h1>"

@app.route('/<string:user>/edit/<int:post_id>')
def edit_post(user, post_id):
    return f"<h1>Edit Blog: {post_id}</h1>"


if __name__ == '__main__':
    app.run(port=5555, debug=True)
