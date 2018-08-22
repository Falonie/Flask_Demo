from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Question
from . import api


@api.route('/posts/<int:id>')
def get_post(id):
    post = Question.query.get_or_404(id)
    # post=Question.query.first(id)
    return jsonify(post.to_json())
