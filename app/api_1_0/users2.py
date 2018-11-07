from flask import render_template
from flask_restful import Api, Resource, fields, marshal_with
from ..models import User
# from . import api_bp
# from .. import api
# from flask import Blueprint

# api_bp = Blueprint('api', __name__)

# resource_fields = {
#     'id': fields.Integer,
#     'username': fields.String
# }
#
#
# class UserResource(Resource):
#     @marshal_with(resource_fields)
#     def get(self, name):
#         user = User.query.filter(User.username == name).first()
#         return user
#
#
# api.add_resource(UserResource, '/user/<name>')
