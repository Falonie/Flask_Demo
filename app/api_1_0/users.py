from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Question


@api.route('/users/<int:id>/')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, int)
    pagination = Question.query.filter(Question.user_id == user.id).order_by(Question.create_time.desc()). \
        paginate(page=page, per_page=2, error_out=False)
    posts = pagination.items
    previous = None
    if pagination.has_prev:
        previous = url_for('api.get_user_posts', id=id, page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page + 1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'next': next,
        'prev': previous
    })
