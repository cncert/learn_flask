# encoding: utf-8
# 业务函数与路由

from flask import jsonify, g,render_template
from . import haha
from ..auth.auth_exts import multi_auth
from .. import db
from ..models import User


@haha.route('/', methods=['GET', 'POST'])  # 不同的蓝本装饰器不同
# @multi_auth.login_required
def hah():
    return render_template('index2/index.html')




