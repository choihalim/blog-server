from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from config import db


class Follower(db.Model, SerializerMixin):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key=True)
    following_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Follower {self.id}>"

    serialize_rules = ("-following_user", "-followed_by_user")


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    posts = relationship('Post', backref='user')
    comments = relationship('Comment', backref='user')

    # Many-to-many relationship: User.followers (following relationship)
    followers_association = relationship(
        "Follower",
        foreign_keys=[Follower.following_user_id],
        backref="following_user"
    )
    followers = association_proxy('followers_association', 'followed_by_user', creator=lambda user: Follower(followed_by_user=user))

    def __repr__(self):
        return f'<User {self.username}>'

    serialize_rules = ("-password", "-posts", "-comments", "-followers")


class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    type = db.Column(db.String)
    tags = db.Column(db.String)
    likes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = relationship("Comment", backref="post")

    def __repr__(self):
        return f'<Post {self.title}>'
    
    def post_info(self):
        serialized = self.to_dict(rules=("-user", "-comments"))
        serialized["username"] = self.user.username if self.user else None
        return serialized
    
    serialize_rules = ("-user", "-comments")


class Comment(db.Model, SerializerMixin):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    likes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment {self.id}>'

    serialize_rules = ("-user", "-post")

