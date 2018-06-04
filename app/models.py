from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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
    last_seen = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        # self.confirmed = True
        # db.session.add(self)
        # return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        # db.session.add(self)
        db.session.commit()
        return True

    def ping(self):
        self.last_seen = datetime.now
        db.session.add(self)
        # db.session.commit()

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

    # def __repr__(self):
    #     return '<Question {}>'.format(self.title)


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

    # def __repr__(self):
    #     return '<Comment {}>'.format(self.content)

# print(User.query().filter().all())
# with app.app_context():
#     print(User.query.filter().all())
#     db.drop_all()
