from flask import jsonify, request, url_for, current_app, g
from .. import db
from ..models import User, Question, Comment
from . import api


@api.route('/comments/<int:id>/')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/questions/<int:id>/comments/')
def get_post_comments(id):
    page = request.args.get('page', 1, int)
    pagination = Comment.query.filter(Comment.question_id == id).paginate(page=page, per_page=
    current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    previous = None
    if pagination.has_prev:
        previous = url_for('api.get_post_comments', id=id, page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_post_comments', id=id, page=page + 1, _external=True)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': previous,
        'next': next
    })


@api.route('/questions/<int:id>/comments/', methods=['POST'])
def new_comment(id):
    comment = Comment.from_json(json_comment=request.json)
    comment.questions = Question.query.get_or_404(id)
    comment.users = g.current_user
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), url_for('api.get_comment', id=comment.id, _external=True)
