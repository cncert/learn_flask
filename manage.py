# encoding: utf-8
import os
from flask_script import Manager
from app1 import app_create
from db_scripts import DBmanager
from flask_migrate import Migrate, MigrateCommand
from app1 import db, socketio  # 新添加支持websocket


app = app_create(os.getenv('FLASK_CONFIG') or 'default')  # 设置启动方式，可选：development、testing、production
manager = Manager(app)
migrate = Migrate(app,db)  # 使用Migrate将app与db关联


# 自定义命令 ，
# 在命令行使用： python manage.py runserver
# @manager.command
# def runserver():
#     print('running')


# 添加额外二级命令
# 第一种方式：自定义命令
# manager.add_command('db',DBmanager)  # 'db'是自定义的命令名字
# 在命令行使用： python manage.py db init  ,init是自定义的函数


# 第二种方式：数据迁移使用MigrateCommand中自带的命令（常用）
# 该模块中带有的命令的使用顺序（顺序不能乱）：
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
manager.add_command('db',MigrateCommand)
manager.add_command('run', socketio.run(app=app, host='0.0.0.0', port=5000))  # 新加入的内容，重写manager的run命令


if __name__ == '__main__':
    manager.run()
