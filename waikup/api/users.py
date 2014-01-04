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
        if not user.check_password(request.form['password']):
            raise ApiError("Invalid credentials", status_code=403)
    except ApiError:
        raise ApiError("Invalid credentials", status_code=403)
    token = user.generate_token()
    data = TokenResource(token).data
    return jsonify(data)


@users.route('/deauth', methods=['POST'])
def deauth():
    from waikup.models import Token
    token_str = request.headers['Auth']
    token = Token.get(Token.token == token_str)
    return jsonify({"success": True})
