import string,random
from flask import url_for, redirect, request, render_template, session, flash,jsonify
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from flask_paginate import Pagination, get_page_parameter
from . import main
from .. import db, mail
from ..models import User, Question, Comment
from .forms import PostForm, CommentForm
from ..decorators import login_required_


@main.route('/')
def index():
    # context = {'questions': Question.query.filter().order_by('-create_time').all()}
    # return render_template('index.html', **context)
    posts = Question.query.filter().order_by('-create_time').all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * 4
    end = start + 4
    post = Question.query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=Question.query.count())
    print(Question.query.count())
    # print(post, type(post))
    return render_template('index.html', questions=post, pagination=pagination)
    # return render_template('index.html', questions=posts)


@main.route('/question/', methods=['GET', 'POST'])
@login_required
# @login_required_
def question():
    form = PostForm(request.form)
    if form.validate():
        post = Question(title=form.title.data, content=form.content.data)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        post.users = user
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    print(form.errors)
    return render_template('question.html')


@main.route('/articles/<question_id>')
def articles(question_id):
    article = Question.query.filter(Question.id == question_id).first()
    return render_template('articles.html', question=article)


@main.route('/comments/', methods=['POST'])
@login_required
# @login_required_
def comments():
    form = CommentForm(request.form)
    if form.validate():
        # comment_content = request.form.get('comment_content')
        comment_content = form.comment_content.data
        comment = Comment(content=comment_content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        comment.users = user
        question_id = request.form.get('question_id')
        question = Question.query.filter(Question.id == question_id).first()
        comment.questions = question
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.articles', question_id=question_id))
    # print('1111111')
    question_id = request.form.get('question_id')
    return redirect(url_for('.articles', question_id=question_id))


@main.route('/profile/<user_name>/')
def profile(user_name):
    # id = session.get('user_id')
    user = User.query.filter(User.username == user_name).first()
    return render_template('profile.html', user=user)