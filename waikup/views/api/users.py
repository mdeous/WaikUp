# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from peewee import DoesNotExist

from waikup.lib import globals as g
from waikup.lib.errors import ApiError
from waikup.lib.helpers import required_fields
from waikup.views.api import Resource, ResourceSet

users = Blueprint('users', __name__)


class UserResource(Resource):
    name = 'user'
    fields = ('username', 'first_name', 'last_name', 'email', 'admin', 'active')


@users.route('/')
@g.auth.admin_required
def list_users():
    """Get all users in database."""
    from waikup.models import User
    user_objs = list(User.select())
    data = ResourceSet(UserResource, user_objs).data
    return jsonify(data)


@users.route('/<int:userid>')
@g.auth.admin_required
def get_user(userid):
    """Get user with given ID."""
    from waikup.models import User
    try:
        user = User.get(User.id == userid)
        data = UserResource(user).data
    except DoesNotExist:
        raise ApiError("User not found: %d" % userid, status_code=404)
    return jsonify(data)


@users.route('/', methods=['POST'])
@g.auth.admin_required
@required_fields('username', 'first_name', 'last_name', 'email', 'password')
def create_user():
    """Create a new user."""
    from waikup.models import User
    user = User.create(
        username=request.form.get('username'),
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        email=request.form.get('email')
    )
    user.set_password(request.form.get('password'))
    user.save()
    return jsonify({"success": True})


@users.route('/<int:userid>', methods=['PUT'])
@g.auth.admin_required
def update_user(userid):
    """Update informations for user with given ID."""
    # TODO: find a way to allow an user to update its own informations
    from waikup.models import User
    user = User.get(User.id == userid)
    user.safe_update(request.form)
    if 'password' in request.form:
        user.set_password(request.form['password'])
        user.save()
    return jsonify({"success": True})


@users.route('/<int:userid>', methods=['DELETE'])
@g.auth.admin_required
def delete_user(userid):
    """Delete user with given ID."""
    from waikup.models import User
    User.safe_delete(User.id == userid)
    return jsonify({"success": True})
