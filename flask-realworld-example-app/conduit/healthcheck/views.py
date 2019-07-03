# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request
import json

blueprint = Blueprint('healthcheck', __name__)
@blueprint.route('/_status', methods=('GET',))
def status():
    return json.dumps("OK")
