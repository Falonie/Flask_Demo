from flask import Flask, url_for, redirect, request, render_template, session,flash
from flask_login import login_required
from . import main
from .. import db
from ..models import User,Question,Comment
from .forms import RegistrationForm
from ..decorators import login_required_

# app = Flask(__name__)
# app.config.from_object(config)
# app.config['SECRET_KEY'] = os.urandom(24)
# db.init_app(app)


# login_required()

@main.route('/')
def index():
    # context = {'questions': Question.query.filter().order_by('-create_time').all()}
    # return render_template('index.html', **context)
    post = Question.query.filter().order_by('-create_time').all()
    # print(post, type(post))
    return render_template('index.html', questions=post)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    telephone = request.form.get('telephone')
    password = request.form.get('password')
    user = User.query.filter(User.telephone == telephone, password == password).first()
    if user:
        session['user_id'] = user.id
        session.permanent = True
        # return 'Success!'
        return redirect(url_for('.index'))


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@main.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User(username=form.username.data, telephone=form.telephone.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    print(form.errors)
    # flash(message='{}'.format(form.errors))
    return render_template('register.html')


@main.route('/question/', methods=['GET', 'POST'])
@login_required
# @login_required_
def question():
    if request.method == 'GET':
        return render_template('question.html')
    title = request.form.get('title')
    content = request.form.get('content')
    question = Question(title=title, content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    question.users = user
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/articles/<question_id>')
def articles(question_id):
    article = Question.query.filter(Question.id == question_id).first()
    return render_template('articles.html', question=article)


@main.route('/comments/', methods=['POST'])
@login_required
# @login_required_
def comments():
    comment_content = request.form.get('comment_content')
    comment = Comment(content=comment_content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.users = user
    question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id == question_id).first()
    comment.questions = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.articles',question_id=question_id))