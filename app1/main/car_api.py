# encoding: utf-8
# 业务函数与路由

from . import main
from .. import db
from ..models import Art
from flask import render_template


@main.route('/cc', methods=['GET', 'POST'])  # 不同的蓝本装饰器不同
def index():
    return render_template('index.html')

