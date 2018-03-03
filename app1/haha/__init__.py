# encoding: utf-8

from flask import Blueprint
# haha = Blueprint('haha', __name__,url_prefix='/haha',static_folder='../../web/index2', template_folder='../../web/index2')
haha = Blueprint('haha', __name__,url_prefix='/haha')
# 在这里指定的是只作用于这一个蓝本的路由。不同的蓝本可以指定不同的静态文件。。。。
# 通过 static_folder 指定静态资源路径，
# 以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
from . import ha_api
# 由于路由和错误处理页面定义在这个文件里面，导入到蓝本把他们关联起来，
# 又因为views.py，error.py需要导入蓝本main，防止循环导入所以放到最后
