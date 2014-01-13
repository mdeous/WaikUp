# -*- coding: utf-8 -*-

from flask import jsonify


class ApiError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

    @property
    def json(self):
        data = {"success": False, "message": self.message}
        return jsonify(data)


def http_error(error):
    response = jsonify({"success": False, "message": getattr(error, 'name', 'Unknown error')})
    response.status_code = getattr(error, 'code', 500)
    return response
