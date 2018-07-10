# encoding: utf-8
# 业务函数与路由

from . import main
from .. import db
from flask import render_template
from ..my_websocket.websockets import *  # 从自定义的websockets文件中导入websocket函数，必须


@main.route('/cc', methods=['GET', 'POST'])  # 不同的蓝本装饰器不同
def index():
    return render_template('index.html')

