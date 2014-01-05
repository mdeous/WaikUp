# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

from waikup.lib import globals as g


webui = Blueprint('webui', __name__)


@webui.route('/')
@g.auth.login_required
def index():
    return render_template('index.html')
