# encoding: utf-8

from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_restful import Api
from flask_cors import CORS # 解决跨域请求
from flask_jwt_extended import JWTManager


mail = Mail()
moment = Moment()
db = SQLAlchemy()
api = Api()
from app1.admin.views import UserApi  # 为了避免循环引用问题，在这里导入
# 初始化app


def app_create(config_name):
    app = Flask(__name__,static_folder='../web/static', template_folder='../web')
    # 通过 static_folder 指定静态资源路径，
    # 以便 index.html 能正确访问 CSS 等静态资源
    # template_folder 指定模板路径，以便 render_template 能正确渲染 index.html
    app.config.from_object(config[config_name])  # 可以直接把对象里面的配置数据转换到app.config里面
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)

    # 路由和其他处理程序定义
    # 注册蓝图
    from .main import main as main_blueprint  # 从当前目录下面的main子目录导入main
    from .admin import admin as admin_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    api.add_resource(UserApi,'/api/users','/api/users/<string:id>',endpoint='users')
    # add_resource 函数使用指定的endpoint 将路由注册到框架上
    api.init_app(app)  # api初始化必须放在路由注册之后
    CORS(app)  # 跨域请求

    return app
