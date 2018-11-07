from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Question
from . import api


@api.route('/questions/')
def get_posts():
    page = request.args.get('page', 1, int)
    pagination = Question.query.order_by(Question.create_time.desc()).paginate(page=page, per_page=
    current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=True)
    posts = pagination.items
    previous = None
    if pagination.has_prev:
        previous = url_for('api.get_posts', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page + 1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': previous,
        'next': next
    })


@api.route('/questions/<int:id>/')
def get_post(id):
    post = Question.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
def new_question():
    question = Question.from_json(json_post=request.json)
    question.users = g.current_user
    db.session.add(question)
    db.session.commit()
    return jsonify(question.to_json()), {'Location': url_for('api.get_post', id=question.id, _external=True)}
