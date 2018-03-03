# encoding: utf-8
# 业务函数与路由

from flask import jsonify, g
from . import main
from ..auth.auth_exts import multi_auth
from .. import db
from ..models import User


@main.route('/s', methods=['GET', 'POST'])  # 不同的蓝本装饰器不同
@multi_auth.login_required
def books():
    return jsonify({"res":1})




