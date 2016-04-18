# -*- coding: utf-8 -*-

from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin, AnonymousUser
from flask.ext.security.utils import verify_password, encrypt_password
from peewee import *

from waikup import settings
from waikup.lib import globals as g


class WaikUpAnonymousUser(AnonymousUser):
    @property
    def is_admin(self):
        return False


class User(UserMixin, g.db.Model):
    id = PrimaryKeyField()
    first_name = CharField()
    last_name = CharField()
    password = CharField()
    email = CharField(unique=True)
    admin = BooleanField(default=False)
    active = BooleanField(default=True)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

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


class Role(RoleMixin, g.db.Model):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    description = TextField(null=True)


class UserRole(g.db.Model):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')

    @property
    def name(self):
        return self.role.name

    @property
    def description(self):
        assert isinstance(self.role, Role)
        return self.role.description


class Category(g.db.Model):
    id = PrimaryKeyField()
    name = CharField(unique=True, default=settings.DEFAULT_CATEGORY)

    def __unicode__(self):
        return u'%s' % self.name


class Link(g.db.Model):
    class Meta(object):
        order_by = ('-submitted',)

    id = PrimaryKeyField()
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


class EMail(g.db.Model):
    id = PrimaryKeyField()
    address = CharField(unique=True)
    disabled = BooleanField(default=False)
