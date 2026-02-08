from datetime import datetime
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="normal_user")  # normal_user, journalist, admin
    is_active = db.Column(db.Boolean, default=True)

    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    likes = db.relationship("Like", backref="user", lazy=True)
    shares = db.relationship("Share", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(20), default="article")  # article, video, photo
    category = db.Column(db.String(80))
    tags = db.Column(db.String(255))  # e.g., "python,web"
    media_url = db.Column(db.String(255))
    thumbnail_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default="draft")  # draft, published
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    comments = db.relationship("Comment", backref="post", lazy=True, cascade="all,delete-orphan")
    likes = db.relationship("Like", backref="post", lazy=True, cascade="all,delete-orphan")
    shares = db.relationship("Share", backref="post", lazy=True, cascade="all,delete-orphan")

    def to_dict(self, include_content=True):
        data = {
            "id": self.id,
            "title": self.title,
            "post_type": self.post_type,
            "category": self.category,
            "tags": self.tags.split(",") if self.tags else [],
            "media_url": self.media_url,
            "thumbnail_url": self.thumbnail_url,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "author_id": self.author_id,
            "likes_count": len(self.likes),
            "shares_count": len(self.shares),
        }
        if include_content:
            data["content"] = self.content
        return data

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))

    replies = db.relationship("Comment")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "post_id": self.post_id,
            "author_id": self.author_id,
            "parent_comment_id": self.parent_comment_id,
        }

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "post_id", name="uq_user_post_like"),
    )

class Share(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(80))
    message = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
