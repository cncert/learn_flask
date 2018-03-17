# encoding: utf-8

from flask import Blueprint
admin = Blueprint('admin', __name__,url_prefix='/admin')  # url的前缀是/admin
from . import views

