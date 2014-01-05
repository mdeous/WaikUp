# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

webui = Blueprint('webui', __name__)


@webui.route('/')
def index():
    return render_template('index.html')
