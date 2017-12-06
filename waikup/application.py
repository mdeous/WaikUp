# -*- coding: utf-8 -*-

from flask import request
from peewee import fn
from werkzeug.contrib.atom import AtomFeed

import settings
from .lib.factory import create_app


# Setup application
app = create_app(settings)


# Atom feed
@app.route('/links.atom')
def links_feed():
    """
    Atom feed view.
    :return: Atom feed HTTP response.
    """
    from .lib.models import Category, Link
    feed_title = 'Recently submitted links'
    cat = request.args.get('cat')
    if cat is not None:
        feed_title += (' - %s' % cat.title())
        category = Category.get(fn.lower(Category.name) == cat.lower())
        all_links = Link.select().where(Link.category == category).limit(settings.ATOM_LINKS_COUNT)
    else:
        all_links = Link.select().limit(settings.ATOM_LINKS_COUNT)
    feed = AtomFeed(
        feed_title,
        feed_url=request.url,
        url=request.base_url
    )
    for link in all_links:
        feed.add(
            link.title,
            unicode(link.description),
            content_type='text',
            author='%s %s' % (link.author.first_name, link.author.last_name),
            url=link.url,
            updated=link.submitted
        )
    return feed.get_response()


# Context processors
@app.context_processor
def global_forms():
    """
    Context processor that defines forms used in every view.
    :return: a {form_name: form_object} dict.
    """
    from .lib.forms import NewLinkForm, ChangePasswordForm
    newlink_form = NewLinkForm()
    newlink_form.set_category_choices()
    return {
        'new_link_form': newlink_form,
        'chpasswd_form': ChangePasswordForm()
    }
