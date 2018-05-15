from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='users')
    comments = db.relationship('Comment', backref='users')
    email = db.Column(db.String(50), unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, telephone, email=None):
        self.username = username
        self.password = password
        self.telephone = telephone
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # users = db.relationship('User', backref='questions')
    comments = db.relationship('Comment', backref=db.backref('questions'))

    # comments = db.relationship('Comment', backref=db.backref('questions',order_by=id.desc()))

    def __repr__(self):
        return '<Question {}>'.format(self.title)


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time = db.Column(db.DateTime, default=datetime.now)

    # questions = db.relationship('Question', backref='comments')
    # users = db.relationship('User', backref='comments')
    # questions = db.relationship('Question', backref=db.backref('comments'))
    # users = db.relationship('User', backref=db.backref('comments'))

    def __repr__(self):
        return '<Comment {}>'.format(self.content)

# print(User.query().filter().all())
# with app.app_context():
#     print(User.query.filter().all())
#     db.drop_all()
