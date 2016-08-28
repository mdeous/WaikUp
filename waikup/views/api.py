# -*- coding: utf-8 -*-

from flask import Blueprint, current_app
from flask_restful import Resource, marshal_with, abort
from flask_restful.fields import Integer, String, DateTime, Boolean, List, Nested
from flask_restful.reqparse import RequestParser
from flask_security import current_user, auth_token_required
from peewee import IntegrityError

from waikup.models import Link, Category

api = Blueprint('api', __name__)

# messages format definitions
link_format = {
    'id': Integer,
    'url': String,
    'title': String,
    'description': String,
    'submitted': DateTime(dt_format='iso8601'),
    'archived': Boolean,
    'author': String,
    'category': String
}
link_message = {
    'success': Boolean,
    'link': Nested(link_format)
}
link_list_message = {
    'success': Boolean,
    'links': List(Nested(link_format))
}
user_format = {
    'id': Integer,
    'first_name': String,
    'last_name': String,
    'email': String,
    'admin': Boolean
}
user_message = {
    'success': Boolean,
    'profile': Nested(user_format)
}


class BaseResource(Resource):
    """
    Base resource class requiring token authentication.
    """
    method_decorators = [auth_token_required]


class LinkResource(BaseResource):
    """
    Resource for unique existing links.
    """
    @marshal_with(link_message)
    def get(self, linkid):
        """
        Gets given link.
        :param linkid: id of the link that should be returned.
        :return: the link corresponding to given id (or an error).
        """
        try:
            link = Link.get(Link.id == linkid)
        except Link.DoesNotExist:
            abort(404, success=False, message='No link with this id: %d' % linkid)
        else:
            return {'success': True, 'link': link}

    def delete(self, linkid):
        """
        Deletes given link.
        :param linkid: id of the link that should be deleted.
        :return: the id of the deleted link (or an error).
        """
        try:
            link = Link.get(Link.id == linkid)
        except Link.DoesNotExist:
            abort(404, success=False, message='No link with this id: %d' % linkid)
        else:
            if (current_user == Link.author) or current_user.is_admin:
                link.delete()
                return {'success': True, 'linkid': linkid}
            abort(403, success=False, message='Unauthorized to delete this link: %d' % linkid)


class LinkListResource(BaseResource):
    """
    Resource for links list.
    """
    @marshal_with(link_list_message)
    def get(self):
        """
        Gets all the links, filtered according to given parameters.
        :return: a list of the filtered links
        """
        get_parser = RequestParser()
        get_parser.add_argument(
            'archived',
            dest='archived',
            type=int,
            choices=(0, 1),
            default=0,
            location='args'
        )
        get_parser.add_argument(
            'search',
            dest='search',
            location='args'
        )
        args = get_parser.parse_args()
        links = Link.select().where(Link.archived == bool(args.archived))
        if args.search is not None:
            pattern = '%%%s%%' % args.search
            links = links.where(
                (Link.url ** pattern) |
                (Link.title ** pattern) |
                (Link.description ** pattern)
            )
        return {'success': True, 'links': links.order_by(Link.id.asc())}

    def post(self):
        """
        Adds a new link.
        :return: the newly created link (or an error).
        """
        post_parser = RequestParser()
        post_parser.add_argument(
            'url',
            dest='url',
            required=True,
            location='form'
        )
        post_parser.add_argument(
            'title',
            dest='title',
            required=True,
            location='form'
        )
        post_parser.add_argument(
            'description',
            dest='description',
            default='No description',
            location='form'
        )
        post_parser.add_argument(
            'category',
            dest='category',
            choices=[cat.name for cat in Category.select()],
            default=current_app.config['DEFAULT_CATEGORY'],
            location='form'
        )
        args = post_parser.parse_args()
        category = Category.select().where(Category.name == args.category)
        try:
            link = Link.create(
                url=args.url,
                title=args.title,
                description=args.description,
                category=category,
                author=current_user
            )
        except IntegrityError:
            abort(409, success=False, message='link already exists: %s' % args.url)
        else:
            return {'success': True, 'linkid': link.id}


class UserResource(BaseResource):
    @marshal_with(user_message)
    def get(self):
        return {'success': True, 'profile': current_user}
