# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request, abort

from waikup.lib import globals as g
from waikup.lib.helpers import required_fields


api = Blueprint('api', __name__)


class Resource(object):
    name = ''
    plural = None
    fields = ()
    fk_map = {}

    def __init__(self, obj):
        self.obj = obj

    @property
    def dict(self):
        result = {}
        for field in self.fields:
            value = getattr(self.obj, field)
            if field in self.fk_map:
                value = getattr(value, self.fk_map[field])
            result[field] = value
        return result

    @property
    def data(self):
        return {"success": True, self.name: self.dict}


class ResourceSet(object):
    def __init__(self, resource_cls, objs):
        self.name = (resource_cls.name + 's') if resource_cls.plural is None else resource_cls.plural
        self.resources = []
        for obj in objs:
            self.resources.append(resource_cls(obj))

    @property
    def data(self):
        result = {"success": True, self.name: []}
        for resource in self.resources:
            result[self.name].append(resource.dict)
        return result


class LinkResource(Resource):
    name = 'link'
    fields = ('id', 'url', 'title', 'description', 'submitted', 'author')
    fk_map = {'author': 'username'}


class CategoryResource(Resource):
    name = 'category'
    plural = 'categories'
    fields = ('id', 'name')


@api.route('/links', methods=['GET'])
@g.api_auth.login_required
def list_links():
    """Get all links in database."""
    from waikup.models import Link
    link_objs = list(Link.select())
    data = ResourceSet(LinkResource, link_objs).data
    return jsonify(data)


@api.route('/links/<int:linkid>', methods=['GET'])
@g.api_auth.login_required
def get_link(linkid):
    """Get link with given ID."""
    from waikup.models import Link
    link = Link.get(Link.id == linkid)
    data = LinkResource(link).data
    return jsonify(data)


@api.route('/links/create', methods=['POST'])
@g.api_auth.login_required
@required_fields('url', 'title')
def create_link():
    """Create a new link."""
    from waikup.models import Link, User
    token = request.headers['Auth']
    user = User.from_token(token)
    link = Link.create(
        url=request.form.get('url'),
        title=request.form.get('title'),
        description=request.form.get('description'),
        author=user
    )
    return jsonify({"success": True})


@api.route('/links/<int:linkid>/update', methods=['POST'])
@g.api_auth.login_required
def update_link(linkid):
    """Update informations for link with given ID."""
    from waikup.models import Link
    link = Link.get(Link.id == linkid)
    token = g.api_auth.get_token()
    if link.author.username != token.user.username:
        abort(403)
    link.safe_update(request.form)
    return jsonify({"success": True})


@api.route('/links/<int:linkid>/delete', methods=['POST'])
@g.api_auth.login_required
def delete_link(linkid):
    """Delete link with given ID."""
    from waikup.models import Link
    link = Link.get(Link.id == linkid)
    token = g.api_auth.get_token()
    if link.author.username != token.user.username:
        abort(403)
    link.delete_instance()
    return jsonify({"success": True})


@api.route('/categories', methods=['GET'])
@g.api_auth.login_required
def list_categories():
    """Get available links categories."""
    from waikup.models import Category
    categories = list(Category.select())
    data = ResourceSet(CategoryResource, categories).data
    return jsonify(data)
