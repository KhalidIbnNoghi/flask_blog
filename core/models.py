from flask_login import UserMixin
from datetime import datetime

from core import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


now = datetime.now()


# Модель пользователя, отвечает за вход, регистрацию и посты
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')

    def __repr__(self) -> str:
        return self.email

# Функция отвечающая за лайк
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

# Функция отвечающая за дизлайк
    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id).delete()

# Функция проверяет поставлен ли лайк
    def has_liked_post(self, post):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

# Модель отвечает за лайки
class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

# Модель отвечает за посты
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), default='1', nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    posted_on=db.Column(db.DateTime,default=now.strftime("%Y-%m-%d %H:%M:%S"))


    def __repr__(self) -> str:
        return self.title

# Модель отвечает за комментариии
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), default='1', nullable=False)
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'), nullable=True)
    posted_on=db.Column(db.DateTime,default=now.strftime("%Y-%m-%d %H:%M:%S"))
    
    def __repr__(self) -> str:
        return self.name
