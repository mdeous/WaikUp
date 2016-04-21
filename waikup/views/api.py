# -*- coding: utf-8 -*-

from flask import Blueprint, current_app
from flask.ext.restful import Resource, marshal_with, abort
from flask.ext.restful.fields import Integer, String, DateTime, Boolean, List, Nested
from flask.ext.restful.reqparse import RequestParser
from flask.ext.security import current_user, auth_token_required
from peewee import IntegrityError

from waikup.models import Link, Category

api = Blueprint('api', __name__)

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


class BaseResource(Resource):
    method_decorators = [auth_token_required]


class LinkResource(BaseResource):
    @marshal_with(link_message)
    def get(self, linkid):
        try:
            link = Link.get(Link.id == linkid)
        except Link.DoesNotExist:
            abort(404, success=False, message='No link with this id: %d' % linkid)
        else:
            return {'success': True, 'link': link}

    def delete(self, linkid):
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
    @marshal_with(link_list_message)
    def get(self):
        return {'success': True, 'links': Link.select().order_by(Link.id.asc())}

    def post(self):
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
