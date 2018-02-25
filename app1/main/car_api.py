# encoding: utf-8
# 业务函数与路由

from . import main
from .. import db
from ..models import Art


@main.route('/', methods=['GET', 'POST'])  # 不同的蓝本装饰器不同
def index():
    return 'hello'
