import logging

from flask import Blueprint, jsonify
from flask.views import MethodView
from flask import request

bp = Blueprint("test", __name__)
LOG = logging.getLogger(__name__)


class APITest(MethodView):
    def get(self):
        LOG.info("[%s]: %s: %s", request.remote_addr, request.method, request.path)
        return jsonify({"version": "1.0.0", "hl": "yani"})


bp.add_url_rule("/", view_func=APITest.as_view("version"))

