#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from datetime import datetime
from flask import Flask, request, make_response, jsonify, session, abort, url_for
from flask_restful import Resource
from sqlalchemy.orm import joinedload
from sqlalchemy import desc


# Local imports
from config import app, db, api
from models import User, Post, Comment, Follower


# gets all of the posts

@app.route('/')
def redirect():
    return redirect(url_for('home'))


@app.route('/home')
def index():
    # posts = Post.query.order_by(desc(Post.created_at)).all()
    posts = Post.query.all()
    if not posts:
        return make_response("Posts not found", 404)

    serialized_posts = [post.post_info() for post in posts]

    response = make_response(jsonify(serialized_posts), 200)
    return response


@app.route('/login', methods=["POST"])
def login():
    if request.method == "POST":
        rq = request.get_json()
        user = User.query.filter(User.username.like(f"%{rq['username']}%"),
                                User.password == rq['password']).first()

        if user:
            session['user_id'] = user.id
            print(session['user_id'])
            return make_response(user.to_dict(), 200)
        else:
            return {'errors': ['Invalid username/password. Please try again.']}, 401


@app.route('/authorize')
def authorize_session():
    user_id = session.get('user_id')
    if not user_id:
        return {'errors': 'You must be logged in to do that. Please log in or make an account.'}, 401
    else:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return make_response(user.to_dict(), 200)


@app.route('/logout', methods=["DELETE"])
def logout():
    if request.method == "DELETE":
        session['user_id'] = None
        return make_response('', 204)


@app.route('/create_account', methods=["POST"])
def create_account():
    if request.method == "POST":
        rq = request.get_json()
        new_user = User(
            username=rq['username'],
            password=rq['password'],
            email=rq['email']
        )
        if new_user:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return make_response(new_user.to_dict(), 201)
        else:
            return {'errors': ['Missing username/password or email. Please try again.']}, 401

# gets all of a user's posts


@app.route('/<string:user>')
def user_page(user):
    posted_user = User.query.filter(User.username == user).first()
    if posted_user is None:
        return make_response("User not found", 404)

    posts = Post.query.join(User).filter(User.username == user).options(
        db.contains_eager(Post.user)).all()
    serialized_posts = [post.post_info() for post in posts]

    response = make_response(jsonify(serialized_posts), 200)
    return response

# gets a user's post by id


@app.route('/<string:user>/<int:post_id>')
def user_post_page(user, post_id):
    post = Post.query.join(User).filter(
        User.username == user, Post.id == post_id
    ).options(db.contains_eager(Post.user)).first()
    
    if post is None:
        return make_response("Post not found", 404)

    response = make_response(jsonify(post.post_info()), 200)
    return response

# following for a specific user
# @app.route('/following/<string:user>')
# def following(user):
#     return f"<h1>{user.username}'s Following Page</h1>"

# followers for a specific user
# @app.route('/followers/<string:user>')
# def followers(user):
#     query_user = User.query.filter(User.username == user).first()
#     if query_user is None:
#         return make_response("User Not Found", 404)
#     followers = query_user.followers_association
#     if followers:
#         for follower in followers:
#             followed_user = follower.followed_by_user
#             print(followed_user.username)
#         print(followers[0].id)
#         print(query_user.id)

#     return f"<h1>{user}'s Followers Page</h1>"

# creates new post for corresponding user


@app.route('/create/<string:user>', methods=["POST"])
def create_post(user):
    creating_user = User.query.filter(User.username == user).first()

    if creating_user is None:
        return make_response("User not found", 404)

    if request.method == "POST":
        title = request.get_json()["title"]
        body = request.get_json()["body"]
        blog_type = request.get_json()["blog_type"]
        tags = request.get_json()["tags"]
        updated_at = datetime.utcnow()
        new_post = Post(
            title=title,
            body=body,
            blog_type=blog_type,
            tags=tags,
            likes=0,
            updated_at=updated_at,
            user_id=creating_user.id
        )

        db.session.add(new_post)
        db.session.commit()

        response = make_response(jsonify(new_post.to_dict()), 201)
        return response

    # return make_response("Not Found", 404)

# updates a user's post


@app.route('/edit/<string:user>/<int:post_id>', methods=["PATCH"])
def edit_post(user, post_id):
    editing_user = User.query.filter(User.username == user).first()
    if editing_user is None:
        return make_response("User not found", 404)

    post = Post.query.filter(
        Post.id == post_id, Post.user_id == editing_user.id).first()
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
        response = make_response("Edited successfully!", 204)
        return response

    return make_response("Not Found", 404)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
