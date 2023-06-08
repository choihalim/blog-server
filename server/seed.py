#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Post, Comment, Follower

fake = Faker()

BLOG_TYPES = [
    "Personal",
    "Technology",
    "Finance",
    "Business"
]

with app.app_context():
    print("Starting seed...")
    # Seed code goes here!

    User.query.delete()
    Post.query.delete()
    Comment.query.delete()
    Follower.query.delete()

    users = []
    for i in range(30):
        u = User(
            username = fake.simple_profile()['username'],
            email = fake.email()
        )
        users.append(u)
    db.session.add_all(users)
    db.session.commit()

    followers = []
    for i in range (20):
        random_user = rc(users)
        f = Follower(
            following_user_id = random_user.id,
            followed_by_user_id = random_user.id
        )
        followers.append(f)
    db.session.add_all(followers)
    db.session.commit()

    posts = []
    for i in range (50):
        random_user = rc(users)
        p = Post(
            title = fake.first_name(),
            body = fake.text(),
            type = rc(BLOG_TYPES),
            tags = fake.text(),
            likes = randint(1, 400),
            user_id = random_user.id
        )
        posts.append(p)
    db.session.add_all(posts)
    db.session.commit()

    comments = []
    for i in range (100):
        random_user = rc(users)
        random_post = rc(posts)
        c = Comment(
            body = fake.text(),
            likes = randint(0, 100),
            user_id = random_user.id,
            post_id = random_post.id
        )
        comments.append(c)
    db.session.add_all(comments)
    db.session.commit()