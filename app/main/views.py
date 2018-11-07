from datetime import datetime
from flask import url_for, redirect, request, render_template, session, jsonify, current_app
from flask_login import login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from . import main
from .. import db, mail
from ..models import User, Question, Comment
from .forms import PostForm, CommentForm, EditProfileForm, EditArticleForm, DeleteArticleForm


@main.route('/')
def index():
    page = request.args.get('page', type=int, default=1)
    print(current_app.config['FLASKY_POSTS_PER_PAGE'])
    pagination = Question.query.order_by(Question.create_time.desc()). \
        paginate(page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    print(f'pagination {pagination}')
    posts = pagination.items
    return render_template('index.html', questions=posts, pagination=pagination)
    # return render_template('index.html', questions=posts)


@main.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    form = PostForm()
    if form.validate():
        post = Question(title=form.title.data, content=form.content.data)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        # post.users = user
        post.users = current_user._get_current_object()
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    print(form.errors)
    return render_template('question.html')


@main.route('/articles/<question_id>')
def articles(question_id):
    article = Question.query.filter(Question.id == question_id).first()
    # print('article is {}'.format(Question.query))
    question = Question.query.get_or_404(question_id)
    # print('question {}'.format(question))
    # print('comments is {}'.format(Question.query.get_or_404(question_id).comments))
    # print('comments2 is {}'.format(Comment.query.filter(Question.id == question_id)))
    page = request.args.get('page', type=int, default=1)
    pagination = Comment.query.filter(Comment.question_id == question_id).order_by(Comment.time.asc()). \
        paginate(page=page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    # pagination = article.comments.order_by(Comment.time.asc()).\
    #     paginate(page=page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    # print(Comment.query.filter(Question.id == question_id).all())
    # print(article.comments)
    comments = pagination.items
    # print(comments)
    # print(current_user, article.users)
    print('*' * 30)
    # print('{}'.format(Comment.query.filter(Comment.question_id == question_id).all()))
    print('{}'.format(article.comments))
    return render_template('articles.html', question=article, comments=comments, pagination=pagination)
    # return render_template('articles.html', question=article, pagination=pagination)
    # return render_template('articles.html', question=article, comments=comments)


@main.route('/comments/', methods=['GET', 'POST'])
@login_required
def comments():
    form = CommentForm()
    if form.validate():
        # comment_content = request.form.get('comment_content')
        comment_content = form.comment_content.data
        comment = Comment(content=comment_content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        comment.users = user
        # comment.users = current_user._get_current_object()
        # question_id = request.form.get('question_id')
        question_id = form.question_id.data
        question = Question.query.filter(Question.id == question_id).first()
        comment.questions = question
        db.session.add(comment)
        db.session.commit()
        # return redirect(url_for('.articles', question_id=question_id))
        return jsonify({"code": 200, "message": ""})
    # question_id = request.form.get('question_id')
    question_id = form.question_id.data
    return redirect(url_for('.articles', question_id=question_id))


@main.route('/delete_comment/<question_id>/<comment_id>/', methods=['GET', 'POST'])
@login_required
def delete_comment(question_id, comment_id):
    # comment_id = request.form.get('comment_id')
    # question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id == question_id).first()
    comment = Comment.query.filter(Comment.id == comment_id).first()
    comment.questions = question
    # comment.users = current_user
    comment.users = User.query.filter(User.id == session.get('user_id')).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.articles', question_id=question_id))


@main.route('/people/<user_name>/')
# @login_required
def profile(user_name):
    # id = session.get('user_id')
    user = User.query.filter(User.username == user_name).first()
    return render_template('profile.html', user=user)


@main.route('/people/<author>/posts/')
def posts(author):
    # posts = Question.query.filter(User.id == current_user.id).all()
    print(author)
    page = request.args.get('page', type=int, default=1)
    print(current_app.config['FLASKY_ARTICLES_PER_PAGE'])
    user = User.query.filter(User.username == author).first()
    print('posts are {}'.format(
        [post.title for post in Question.query.filter(Question.user_id == user.id).order_by().all()]))
    print('postss are {}'.format([post.title for post in user.questions]))
    pagination = Question.query.filter(Question.user_id == user.id).order_by(Question.create_time.desc()). \
        paginate(page=page, per_page=current_app.config['FLASKY_ARTICLES_PER_PAGE'], error_out=False)
    print('pagination is {}'.format(pagination))
    posts = pagination.items
    # print('posts titles are {}'.format([post.title for post in user.questions]))
    print(
        'posts titles are {}'.format([post.title for post in Question.query.filter(Question.user_id == user.id).all()]))
    post1 = Question.query.filter(Question.user_id == user.id).first()
    post2 = Question.query.filter(User.id == user.id).first()
    print('posts2 {}'.format(post2))
    print('posts2 username {}'.format(post2.users.username))
    post = Question.query.filter(Question.user_id == user.id).all()
    # print('post {}'.format([post]))
    # print('post0 username {}'.format([post][0].username))
    return render_template('posts.html', posts=posts, pagination=pagination, post=[post], author=author)
    # return render_template('posts.html', posts=posts, pagination=pagination, post1=post2)
    # return render_template('posts.html', posts=posts, pagination=pagination, post1=post1)


@main.route('/people/<author>/posts/<post_id>/')
def post(author, post_id):
    post = Question.query.filter(Question.id == post_id).first()
    # user = User.query.filter(User.username == author).first()
    return render_template('post.html', question=post)


@main.route('/edit_post/<article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    form = EditArticleForm()
    article = Question.query.filter(Question.id == article_id).first()
    if form.validate():
        article.title = form.title.data
        article.content = form.content.data
        article.update_time = datetime.now()
        db.session.commit()
        # return redirect(url_for('.posts', post_id=article.id))
        return redirect(url_for('.post', author=article.users.username, post_id=article.id))
    form.title.data = article.title
    form.content.data = article.content
    return render_template('edit_article.html', article=article)


@main.route('/delete_article/<int:article_id>/', methods=['GET', 'POST'])
def delete_article(article_id):
    question = Question.query.filter(Question.id == article_id).first()
    comments = Comment.query.filter(Comment.question_id == article_id).all()
    # question.comments = comments
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('.index'))


@main.route('/editprofile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if form.validate():
        current_user.username = form.name.data
        db.session.commit()
        return redirect(url_for('.profile', user_name=current_user.username))
    form.name.data = current_user.username
    return render_template('edit_profile.html')
