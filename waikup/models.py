# -*- coding: utf-8 -*-

from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin
from flask.ext.security.utils import verify_password, encrypt_password
from peewee import *

from waikup import settings
from waikup.lib import globals as g
from waikup.lib.errors import ApiError


class BaseModel(g.db.Model):
    safe_fields = ()
    id = PrimaryKeyField()
    no_item_code = 404
    no_item_message = "Item does not exist"

    def safe_update(self, data):
        for field in self.safe_fields:
            if (field in data) and (data[field] is not None):
                setattr(self, field, data[field])
        try:
            result = self.save()
        except IntegrityError:
            raise ApiError("Item values overlap with an existing one")
        return result

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            obj = super(BaseModel, cls).get(*args, **kwargs)
        except DoesNotExist:
            raise ApiError(cls.no_item_message, status_code=cls.no_item_code)
        return obj

    @classmethod
    def create(cls, *args, **kwargs):
        try:
            result = super(BaseModel, cls).create(*args, **kwargs)
        except IntegrityError:
            raise ApiError("Item already exists")
        return result

    @classmethod
    def safe_delete(cls, *args, **kwargs):
        try:
            delete_query = cls.delete().where(*args, **kwargs)
            result = delete_query.execute()
        except DoesNotExist:
            raise ApiError(cls.no_item_message, status_code=cls.no_item_code)
        return result


class User(BaseModel, UserMixin):
    safe_fields = (
        'first_name',
        'last_name',
        'email'
    )
    no_item_message = "User does not exist"
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    email = CharField()
    admin = BooleanField(default=False)
    active = BooleanField(default=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def is_active(self):
        return self.active

    def get_id(self):
        return unicode(self.id)

    @property
    def is_admin(self):
        return self.admin

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def set_password(self, password):
        self.password = encrypt_password(password)

    def check_password(self, password):
        return verify_password(password, self.password)


class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)


class UserRole(BaseModel):
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')

    @property
    def name(self):
        return self.role.name

    @property
    def description(self):
        assert isinstance(self.role, Role)
        return self.role.description


class Category(BaseModel):
    name = CharField(unique=True, default=settings.DEFAULT_CATEGORY)

    def __unicode__(self):
        return u'%s' % self.name


class Link(BaseModel):
    class Meta(object):
        order_by = ('-submitted',)

    safe_fields = (
        'url',
        'title',
        'description',
        'archived'
    )
    url = CharField(unique=True)
    title = CharField()
    description = TextField(default='No description')
    submitted = DateTimeField(default=datetime.now)
    archived = BooleanField(default=False)
    author = ForeignKeyField(User, related_name='links')
    category = ForeignKeyField(
        Category,
        related_name='links',
        null=True,
    )

    def __unicode__(self):
        return u'%s' % self.url

    @classmethod
    def toggle_archiving(cls, linkid):
        links = list(cls.select().where(cls.id == linkid))
        if not links:
            return False
        link = links[0]
        link.archived = not link.archived
        link.save()
        return True
