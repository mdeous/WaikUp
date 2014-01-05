# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from waikup.lib import globals as g
from waikup.models import Link


webui = Blueprint('webui', __name__)


@webui.route('/')
@g.auth.login_required
def list_links():
    links = Link.select()
    return render_template(
        'list_links.html',
        links=links
    )
