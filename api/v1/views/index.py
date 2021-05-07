#!/usr/bin/python3
"""
Index for our web flask
"""
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """
    Return json status of web flask
    """
    return """{
    "status": "OK"
    }
    """
