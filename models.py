from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

# =====================

# 用户表

# =====================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    username = db.Column(

        db.String(50),

        unique=True,

        nullable=False

    )

    email = db.Column(

        db.String(100),

        unique=True,

        nullable=False

    )

    password = db.Column(

        db.String(255),

        nullable=False

    )

    avatar = db.Column(

        db.String(255),

        default="default.png"

    )

    create_time = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )

    posts = db.relationship(

        "Post",

        backref="author",

        lazy=True

    )

# =====================

# 分类表

# =====================

class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    name = db.Column(

        db.String(50),

        unique=True,

        nullable=False

    )

    posts = db.relationship(

        "Post",

        backref="category",

        lazy=True

    )

# =====================

# 文章表

# =====================

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    title = db.Column(

        db.String(200),

        nullable=False

    )

    content = db.Column(

        db.Text,

        nullable=False

    )

    cover = db.Column(

        db.String(255),

        default="default.jpg"

    )

    views = db.Column(

        db.Integer,

        default=0

    )

    create_time = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )

    update_time = db.Column(

        db.DateTime,

        default=datetime.utcnow,

        onupdate=datetime.utcnow

    )

    user_id = db.Column(

        db.Integer,

        db.ForeignKey("users.id"),

        nullable=False

    )

    category_id = db.Column(

        db.Integer,

        db.ForeignKey("categories.id")

    )

    comments = db.relationship(

        "Comment",

        backref="post",

        cascade="all, delete"

    )

    likes = db.relationship(

        "Like",

        backref="post",

        cascade="all, delete"

    )

# =====================

# 评论表

# =====================

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    content = db.Column(

        db.Text,

        nullable=False

    )

    create_time = db.Column(

        db.DateTime,

        default=datetime.utcnow

    )

    user_id = db.Column(

        db.Integer,

        db.ForeignKey("users.id")

    )

    post_id = db.Column(

        db.Integer,

        db.ForeignKey("posts.id")

    )

    user = db.relationship(

        "User"

    )

# =====================

# 点赞表

# =====================

class Like(db.Model):

    __tablename__ = "likes"

    id = db.Column(

        db.Integer,

        primary_key=True

    )

    user_id = db.Column(

        db.Integer,

        db.ForeignKey("users.id")

    )

    post_id = db.Column(

        db.Integer,

        db.ForeignKey("posts.id")

    )

    user = db.relationship(

        "User"

    )