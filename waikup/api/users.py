# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from peewee import DoesNotExist

from waikup.api import Resource
from waikup.lib.errors import ApiError
from waikup.lib.helpers import required_fields

users = Blueprint('users', __name__)


class UserResource(Resource):
    name = 'user'
    fields = ('username', 'first_name', 'last_name', 'email', 'admin', 'active')


class TokenResource(Resource):
    name = 'token'
    fields = ('token', 'user')
    fk_map = {'user': 'username'}


@users.route('/auth', methods=['POST'])
@required_fields('username', 'password')
def auth():
    from waikup.models import User
    try:
        user = User.get(User.username == request.form['username'])
    except DoesNotExist:
        raise ApiError("Invalid credentials", status_code=403)
    token = user.generate_token()
    data = TokenResource(token).data
    return jsonify(data)


@users.route('/deauth', methods=['POST'])
def deauth():
    from waikup.models import Token
    token_str = request.headers['Auth']
    try:
        token = Token.get(Token.token == token_str)
        token.delete_instance()
    except DoesNotExist:
        raise ApiError("Invalid token")
    return jsonify({"success": True})
