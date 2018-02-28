# encoding: utf-8

from . import admin
from flask import request,abort,jsonify,g,url_for
from app1 import db
from app1.models import *


@admin.route('/c', methods=['GET', 'POST'])
def ad():
    return 'yes'


@admin.route('/adduser', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    user.generate_auth_token(username)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}





