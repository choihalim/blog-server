#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, jsonify
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

# following for a specific user
@app.route('/following/<string:user>')
def following(user):
    return f"<h1>{user.username}'s Following Page</h1>"

# followers for a specific user
@app.route('/followers/<string:user>')
def followers(user):
    query_user = User.query.filter(User.username == user).first()
    if query_user is None:
        return make_response("User Not Found", 404)
    followers = query_user.followers_association
    print(followers)
    if followers:
        for follower in followers:
            print(follower.following_user.username)
        print(followers[0].id)
    return f"<h1>{user}'s Followers Page</h1>"

# creates new post for corresponding user
@app.route('/create/<string:user>', methods=["POST"])
def create_post(user):
    creating_user = User.query.filter(User.username == user).first()

    if creating_user is None:
        return make_response("User not found", 404)
    
    if request.method == "POST":
        title = request.get_json()["title"]
        body = request.get_json()["body"]
        type = request.get_json()["type"]
        tags = request.get_json()["tags"]
        new_post = Post(
            title=title,
            body=body,
            type=type,
            tags=tags,
            likes=0,
            user_id=creating_user.id
        )

        db.session.add(new_post)
        db.session.commit()

        response = make_response(jsonify(new_post.to_dict()), 201)
        return response
    
    return make_response("Not Found", 404)

# updates a user's post
@app.route('/edit/<string:user>/<int:post_id>', methods=["PATCH"])
def edit_post(user, post_id):
    editing_user = User.query.filter(User.username == user).first()
    if editing_user is None:
        return make_response("User not found", 404)
    
    post = Post.query.filter(Post.id == post_id, Post.user_id == editing_user.id).first()
    if post is None:
        return make_response("Post not found", 404)
    
    if request.method == "PATCH":
        title = request.get_json()["title"]
        body = request.get_json()["body"]
        type = request.get_json()["type"]
        tags = request.get_json()["tags"]
        if title:
            post.title = title
        if body:
            post.body = body
        if type:
            post.type = type
        if tags:
            post.tags = tags

        db.session.commit()
        response = make_response("", 204)
        return response

    return make_response("Not Found", 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
