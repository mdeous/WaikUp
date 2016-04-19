# -*- coding: utf-8 -*-

from flask import Blueprint, current_app
from flask.ext.restful import Resource, marshal_with, abort
from flask.ext.restful.fields import Integer, String, DateTime, Boolean, List, Nested
from flask.ext.restful.reqparse import RequestParser
from peewee import DoesNotExist, IntegrityError

from waikup.models import Link, Category, User

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


class LinkResource(Resource):
    @marshal_with(link_message)
    def get(self, linkid):
        try:
            return {'success': True, 'link': Link.get(Link.id == linkid)}
        except DoesNotExist:
            abort(404, success=False, message='No link with id %d' % linkid)

    def delete(self, linkid):
        try:
            link = Link.get(Link.id == linkid)
        except DoesNotExist:
            abort(404, success=False, message='No link with id %d' % linkid)
        else:
            link.delete()
            return {'success': True, 'linkid': linkid}


class LinkListResource(Resource):
    @marshal_with(link_list_message)
    def get(self):
        return {'success': True, 'links': Link.select()}

    def post(self):
        parser = RequestParser()
        parser.add_argument(
            'url',
            dest='url',
            required=True
        )
        parser.add_argument(
            'title',
            dest='title',
            required=True
        )
        parser.add_argument(
            'description',
            dest='description',
            default='No description'
        )
        parser.add_argument(
            'category',
            dest='category',
            choices=[cat.name for cat in Category.select()],
            default=current_app.config['DEFAULT_CATEGORY']
        )
        args = parser.parse_args()
        category = Category.select().where(Category.name == args.category)
        try:
            link = Link.create(
                url=args.url,
                title=args.title,
                description=args.description,
                category=category,
                author=User.get(User.id == 1)
            )
        except IntegrityError:
            abort(409, success=False, message='link already exists: %s' % args.url)
        else:
            return {'success': True, 'linkid': link.id}
