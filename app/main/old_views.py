from flask import Flask, url_for, redirect, request, render_template, session
from . import main
from .. import db
from ..models import User,Question,Comment
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
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    telephone = request.form.get('telephone')
    password = request.form.get('password')
    repeat_password = request.form.get('repeat_password')
    user = User.query.filter(User.telephone == telephone).first()
    if user:
        # flash('该手机号已被注册')
        return '该手机号已被注册'
    # else:
    if password != repeat_password:
        # flash('密码不一致')
        return '密码不一致'
    # else:
    u = User(telephone=telephone, username=username, password=password)
    db.session.add(u)
    db.session.commit()
    return redirect(url_for('.login'))


@main.route('/question/', methods=['GET', 'POST'])
@login_required_
# @login_required
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
@login_required_
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


# class CommentView(views.MethodView):
#     decorators = [login_required]
#
#     def get(self):
#         question_id = request.form.get('question_id')
#         return redirect(url_for('.articles', question_id=question_id))
#
#     def post(self):
#         form = CommentForm(request.form)
#         if form.validate():
#             # comment_content = request.form.get('comment_content')
#             comment_content = form.comment_content.data
#             comment = Comment(content=comment_content)
#             user_id = session.get('user_id')
#             user = User.query.filter(User.id == user_id).first()
#             comment.users = user
#             question_id = request.form.get('question_id')
#             question = Question.query.filter(Question.id == question_id).first()
#             comment.questions = question
#             db.session.add(comment)
#             db.session.commit()
#             # return redirect(url_for('.articles', question_id=question_id))
#             return jsonify({"code": 200, "message": ""})
#         return self.get()
#
#
# main.add_url_rule('/comments/', view_func=CommentView.as_view('comments'))

# @main.route('/')
# def index():
#     # context = {'questions': Question.query.filter().order_by('-create_time').all()}
#     # return render_template('index.html', **context)
#     # posts = Question.query.filter().order_by('-create_time').all()
#     # posts = Question.query.filter().all()
#     page = request.args.get(get_page_parameter(), type=int, default=1)
#     start = (page - 1) * 4
#     end = start + 4
#     post = Question.query.slice(start, end)
#     pagination = Pagination(bs_version=3, page=page, total=Question.query.count())
#     # print(Question.query.count())
#     # print(post, type(post))
#     print(current_app.config['FLASKY_POSTS_PER_PAGE'])
#     return render_template('index.html', questions=post, pagination=pagination)
#     # return render_template('index.html', questions=posts)
