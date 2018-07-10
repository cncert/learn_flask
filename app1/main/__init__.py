# encoding: utf-8

from flask import Blueprint
# main = Blueprint('main', __name__,url_prefix='/login',static_folder='../../web/static', template_folder='../../web')
main = Blueprint('main', __name__)
# 不同的蓝本可以指定不同的静态文件。。。。
# 通过 static_folder 指定静态资源路径，
# 以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
from . import car_api, errors,book_api
# 由于路由和错误处理页面定义在这个文件里面，导入到蓝本把他们关联起来，
# 又因为views.py，error.py需要导入蓝本main，防止循环导入所以放到最后
